#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import subprocess
from dataclasses import dataclass
from pathlib import Path


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _signal_id() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


def parse_yaml_list_of_maps(text: str, list_key: str) -> list[dict]:
    """Parse a tiny YAML subset: `{list_key}:` followed by `- key: value` items.

    Supported:
    - top-level `list_key:`
    - list items as maps
    - nested `links:` list of strings

    This is not a general YAML parser.
    """

    lines = text.splitlines()
    in_list = False
    items: list[dict] = []
    cur: dict | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        raw = line.rstrip("\n")
        stripped = raw.strip()
        i += 1

        if not stripped or stripped.startswith("#"):
            continue

        if not in_list:
            if stripped == f"{list_key}:":
                in_list = True
            continue

        # Item start
        if stripped.startswith("-") and ":" in stripped:
            # Close previous
            if cur is not None:
                items.append(cur)
            cur = {}

            # Parse "- key: value"
            after = stripped[1:].strip()
            k, v = after.split(":", 1)
            cur[k.strip()] = _strip_quotes(v.strip())
            continue

        if cur is None:
            continue

        # links list
        if stripped == "links:" or stripped == "depends_on:":
            key = stripped[:-1]
            cur.setdefault(key, [])
            # consume following "- item" lines with greater indent
            while i < len(lines):
                nxt = lines[i]
                nxt_raw = nxt.rstrip("\n")
                nxt_stripped = nxt_raw.strip()
                if not nxt_stripped or nxt_stripped.startswith("#"):
                    i += 1
                    continue
                if not nxt_stripped.startswith("-"):
                    break
                cur[key].append(_strip_quotes(nxt_stripped[1:].strip()))
                i += 1
            continue

        # key: value
        if ":" in stripped:
            k, v = stripped.split(":", 1)
            cur[k.strip()] = _strip_quotes(v.strip())

    if cur is not None:
        items.append(cur)
    return items


@dataclass(frozen=True)
class Plan:
    id: str
    title: str
    kind: str
    mode: str
    status: str
    owner: str
    domain: str
    priority: str
    links: list[str]
    depends_on: list[str]
    notes: str


def load_plans(root: Path) -> list[Plan]:
    path = root / "tools" / "plan-registry" / "plans.yaml"
    items = parse_yaml_list_of_maps(_read_text(path), "plans")
    out: list[Plan] = []
    for it in items:
        out.append(
            Plan(
                id=str(it.get("id", "")),
                title=str(it.get("title", "")),
                kind=str(it.get("kind", "plan")),
                mode=str(it.get("mode", "phase")),
                status=str(it.get("status", "pending")),
                owner=str(it.get("owner", "unassigned")),
                domain=str(it.get("domain", "unassigned")),
                priority=str(it.get("priority", "medium")),
                links=list(it.get("links", []) or []),
                depends_on=list(it.get("depends_on", []) or []),
                notes=str(it.get("notes", "")),
            )
        )
    return out


def _read_budgets(root: Path) -> dict:
    # Minimal YAML-ish key parser for .substrate/constants/budgets.yaml.
    path = root / ".substrate" / "constants" / "budgets.yaml"
    defaults = {"max_in_progress_per_domain": 2, "max_leases_per_domain": 2}
    if not path.exists():
        return defaults
    out = dict(defaults)
    for line in _read_text(path).splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue
        k, v = s.split(":", 1)
        k = k.strip()
        v = _strip_quotes(v.strip())
        if k in out:
            try:
                out[k] = int(v)
            except Exception:
                pass
    return out


def _count_in_progress_by_domain(plans: list[Plan]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in plans:
        if p.status != "in_progress":
            continue
        counts[p.domain] = counts.get(p.domain, 0) + 1
    return counts


def _update_plan_registry(root: Path, plan_id: str, *, status: str | None, owner: str | None) -> bool:
    """Best-effort update of tools/plan-registry/plans.yaml.

    Guarantees:
    - Updates the first `status:` / `owner:` in the target item.
    - Removes duplicate `status:` / `owner:` lines in the target item.
    - Inserts the field if missing.
    """

    path = root / "tools" / "plan-registry" / "plans.yaml"
    lines = _read_text(path).splitlines(True)

    # Find the item region.
    start = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not (s.startswith("-") and "id:" in s):
            continue
        try:
            after = s[1:].strip()
            k, v = after.split(":", 1)
            if k.strip() != "id":
                continue
            cur_id = _strip_quotes(v.strip())
        except Exception:
            continue
        if cur_id == plan_id:
            start = i
            break

    if start is None:
        return False

    end = len(lines)
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if s.startswith("-") and "id:" in s:
            end = j
            break

    item_lines = lines[start:end]
    indent = " " * (len(item_lines[0]) - len(item_lines[0].lstrip(" ")) + 2)

    def rewrite_key(key: str, value: str | None) -> tuple[list[str], bool]:
        if value is None:
            return item_lines, False

        out: list[str] = []
        seen = False
        changed = False
        key_prefix = f"{key}:"
        for ln in item_lines:
            stripped = ln.strip()
            if stripped.startswith(key_prefix):
                if not seen:
                    out.append(f"{indent}{key}: \"{value}\"\n")
                    if stripped != f"{key}: \"{value}\"":
                        changed = True
                    seen = True
                else:
                    # Drop duplicates.
                    changed = True
                continue
            out.append(ln)

        if not seen:
            # Insert right after title if present; else after id.
            insert_at = 1
            for idx, ln in enumerate(out):
                if ln.strip().startswith("title:"):
                    insert_at = idx + 1
                    break
            out[insert_at:insert_at] = [f"{indent}{key}: \"{value}\"\n"]
            changed = True
        return out, changed

    new_lines, c1 = rewrite_key("status", status)
    item_lines = new_lines
    new_lines, c2 = rewrite_key("owner", owner)
    item_lines = new_lines

    if not (c1 or c2):
        return False

    lines[start:end] = item_lines
    _write_text(path, "".join(lines))
    return True


def _touch_state_tracker(root: Path) -> None:
    path = root / "tools" / "state-tracker" / "state.yaml"
    lines = _read_text(path).splitlines(True)
    for i, line in enumerate(lines):
        if line.strip().startswith("last_updated:"):
            indent = line[: len(line) - len(line.lstrip(" "))]
            lines[i] = f"{indent}last_updated: \"{_utc_now_rfc3339()}\"\n"
            _write_text(path, "".join(lines))
            return

    # If missing, append.
    lines.append(f"last_updated: \"{_utc_now_rfc3339()}\"\n")
    _write_text(path, "".join(lines))


def _emit_signal(
    root: Path,
    *,
    kind: str,
    topic: str,
    claim: str,
    from_: str,
    to: str,
    urgency: str = "normal",
    evidence: list[str] | None = None,
    asks: list[str] | None = None,
    next_actions: list[str] | None = None,
    expects_response: bool = False,
    response_by: str = "",
) -> Path:
    out_dir = root / ".bridges" / "signals"
    out_dir.mkdir(parents=True, exist_ok=True)

    sig = {
        "header": {
            "id": _signal_id(),
            "timestamp": _utc_now_rfc3339(),
            "from": from_,
            "to": to,
            "kind": kind,
            "urgency": urgency,
        },
        "body": {
            "topic": topic,
            "claim": claim,
            "evidence": evidence or [],
            "confidence": "high",
            "asks": asks or [],
            "next_actions": next_actions or [],
        },
        "footer": {
            "expects_response": expects_response,
            "response_by": response_by,
        },
    }

    fname = f"{sig['header']['id']}_{kind}_{topic.replace(' ', '_')}.json"
    path = out_dir / fname
    path.write_text(json.dumps(sig, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_state(root: Path) -> dict:
    state_path = root / "tools" / "state-tracker" / "state.yaml"
    # Parse as a small key:value map (no nesting expected here).
    state: dict[str, str] = {}
    for line in _read_text(state_path).splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue
        k, v = s.split(":", 1)
        state[k.strip()] = _strip_quotes(v.strip())

    health_path = root / ".substrate" / "state" / "health.json"
    health = None
    if health_path.exists():
        try:
            health = json.loads(_read_text(health_path))
        except Exception:
            health = None
    return {"state": state, "health": health}


def _priority_rank(p: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(p, 1)


def _domain_rank(d: str) -> int:
    # A sane default ordering for systems work.
    return {"guardian": 0, "watcher": 1, "builder": 2, "scribe": 3, "gems": 4}.get(d, 9)


def suggest_next(plans: list[Plan]) -> list[Plan]:
    candidates = [p for p in plans if p.status in ("pending", "blocked")]
    candidates.sort(key=lambda p: (_priority_rank(p.priority), _domain_rank(p.domain), p.id))
    return candidates


def suggest_active(plans: list[Plan]) -> list[Plan]:
    candidates = [p for p in plans if p.status == "in_progress"]
    candidates.sort(key=lambda p: (_priority_rank(p.priority), _domain_rank(p.domain), p.id))
    return candidates


def cmd_status(args: argparse.Namespace) -> int:
    root = _resolve_root()
    data = load_state(root)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return 0

    state = data.get("state") or {}
    health = data.get("health") or {}
    out = {
        "phase": state.get("phase"),
        "health": health.get("health"),
        "quarantined_units": (health.get("autofile") or {}).get("quarantined_units"),
        "blobs": (health.get("autofile") or {}).get("blobs"),
        "units": (health.get("autofile") or {}).get("units"),
    }
    print(json.dumps(out, indent=2))
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    root = _resolve_root()
    plans = load_plans(root)
    nxt = suggest_next(plans)
    if args.kind:
        nxt = [p for p in nxt if p.kind == args.kind]

    if args.json:
        print(json.dumps([p.__dict__ for p in nxt], indent=2, sort_keys=True))
        return 0

    # Human friendly (still plain).
    lines = []
    for p in nxt[: args.limit]:
        tag = "REV" if p.mode == "revolution" else "PH"
        lines.append(f"{p.id} ({p.kind}/{tag}) [{p.domain}/{p.priority}] {p.title} ({p.status})")
    print("\n".join(lines))
    return 0


def cmd_active(args: argparse.Namespace) -> int:
    root = _resolve_root()
    plans = load_plans(root)
    act = suggest_active(plans)
    if args.kind:
        act = [p for p in act if p.kind == args.kind]

    if args.json:
        print(json.dumps([p.__dict__ for p in act], indent=2, sort_keys=True))
        return 0

    lines = []
    for p in act[: args.limit]:
        tag = "REV" if p.mode == "revolution" else "PH"
        lines.append(f"{p.id} ({p.kind}/{tag}) [{p.domain}/{p.priority}] {p.title} ({p.status})")
    print("\n".join(lines))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    root = _resolve_root()

    updated = _update_plan_registry(root, args.plan_id, status=args.status, owner=args.owner)
    if not updated:
        raise SystemExit(f"plan not found or unchanged: {args.plan_id}")

    _touch_state_tracker(root)

    # Emit a signal for cross-agent visibility.
    from_ = args.from_ or "scribe"
    to = args.to or "all"
    _emit_signal(
        root,
        kind="proclamation",
        topic="plan",
        claim=f"Set {args.plan_id} status={args.status}" + (f" owner={args.owner}" if args.owner else ""),
        from_=from_,
        to=to,
    )

    print(json.dumps({"ok": True, "plan_id": args.plan_id, "status": args.status, "owner": args.owner or ""}, indent=2))
    return 0


def cmd_assign(args: argparse.Namespace) -> int:
    """Assign a work item with just-enough context.

    Steps:
    - generate a context capsule and link it
    - set owner + status=in_progress
    - emit a missive to the assignee with capsule path as evidence
    """

    root = _resolve_root()
    plan_id = args.plan_id
    owner = args.owner
    if not owner:
        raise SystemExit("--owner is required")

    # Enforce in_progress budget per domain (atomic autonomy guardrail).
    plans = load_plans(root)
    target = next((p for p in plans if p.id == plan_id), None)
    if target is None:
        raise SystemExit(f"unknown plan: {plan_id}")
    budgets = _read_budgets(root)
    max_in_progress = int(budgets.get("max_in_progress_per_domain", 2))
    counts = _count_in_progress_by_domain(plans)
    current = counts.get(target.domain, 0)
    if current >= max_in_progress and not args.override:
        raise SystemExit(
            f"in_progress budget exceeded for domain={target.domain} ({current}/{max_in_progress}); use --override with --reason or open a council_call"
        )

    if current >= max_in_progress and args.override and not args.reason:
        raise SystemExit("--override requires --reason")

    updated = _update_plan_registry(root, plan_id, status="in_progress", owner=owner)
    if not updated:
        raise SystemExit(f"plan not found or unchanged: {plan_id}")
    _touch_state_tracker(root)

    # Generate capsule via the context tool (after assignment so metadata is accurate).
    context_cmd = [str(root / "scripts" / "context"), "make", plan_id]
    cp = subprocess.run(context_cmd, check=True, capture_output=True, text=True)
    capsule_path = cp.stdout.strip().splitlines()[-1]
    try:
        capsule_rel = str(Path(capsule_path).resolve().relative_to(root))
    except Exception:
        capsule_rel = capsule_path

    from_ = args.from_ or "scribe"
    to = args.to or owner
    _emit_signal(
        root,
        kind="missive",
        topic="assignment",
        claim=f"Assigned {plan_id} to {owner} (context capsule generated)" + (
            f"; override_reason={args.reason}" if args.override and args.reason else ""
        ),
        from_=from_,
        to=to,
        evidence=[capsule_rel],
        asks=["Acknowledge and proceed", "Emit a dead_end or stub if blocked"],
        next_actions=[f"Read {capsule_rel}", f"Work the item: {plan_id}"],
        expects_response=True,
    )

    if args.override and args.reason:
        _emit_signal(
            root,
            kind="council_call",
            topic="budget_override",
            claim=f"Budget override used for domain={target.domain} on {plan_id}: {args.reason}",
            from_=from_,
            to="council",
            urgency="high",
            evidence=[capsule_rel],
            expects_response=False,
        )

    print(json.dumps({"ok": True, "plan_id": plan_id, "owner": owner, "status": "in_progress", "capsule": capsule_rel}, indent=2))
    return 0


def cmd_budgets(args: argparse.Namespace) -> int:
    root = _resolve_root()
    plans = load_plans(root)
    budgets = _read_budgets(root)
    counts = _count_in_progress_by_domain(plans)
    out = {
        "budgets": budgets,
        "in_progress_by_domain": counts,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    args.status = "in_progress"
    return cmd_set(args)


def cmd_done(args: argparse.Namespace) -> int:
    args.status = "done"
    return cmd_set(args)


def cmd_block(args: argparse.Namespace) -> int:
    args.status = "blocked"
    return cmd_set(args)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="orchestrator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="show state/health summary")
    p_status.add_argument("--json", action="store_true")
    p_status.set_defaults(fn=cmd_status)

    p_next = sub.add_parser("next", help="show suggested next plans")
    p_next.add_argument("--json", action="store_true")
    p_next.add_argument("--limit", type=int, default=25)
    p_next.add_argument("--kind", choices=["plan", "issue", "bug", "dead_end", "stub"])
    p_next.set_defaults(fn=cmd_next)

    p_active = sub.add_parser("active", help="list in_progress work")
    p_active.add_argument("--json", action="store_true")
    p_active.add_argument("--limit", type=int, default=50)
    p_active.add_argument("--kind", choices=["plan", "issue", "bug", "dead_end", "stub"])
    p_active.set_defaults(fn=cmd_active)

    p_set = sub.add_parser("set", help="set a plan status/owner")
    p_set.add_argument("plan_id")
    p_set.add_argument("status", choices=["pending", "in_progress", "blocked", "done"])
    p_set.add_argument("--owner")
    p_set.add_argument("--from", dest="from_")
    p_set.add_argument("--to")
    p_set.set_defaults(fn=cmd_set)

    p_start = sub.add_parser("start", help="mark plan in_progress")
    p_start.add_argument("plan_id")
    p_start.add_argument("--owner")
    p_start.add_argument("--from", dest="from_")
    p_start.add_argument("--to")
    p_start.set_defaults(fn=cmd_start)

    p_done = sub.add_parser("done", help="mark plan done")
    p_done.add_argument("plan_id")
    p_done.add_argument("--owner")
    p_done.add_argument("--from", dest="from_")
    p_done.add_argument("--to")
    p_done.set_defaults(fn=cmd_done)

    p_block = sub.add_parser("block", help="mark plan blocked")
    p_block.add_argument("plan_id")
    p_block.add_argument("--owner")
    p_block.add_argument("--from", dest="from_")
    p_block.add_argument("--to")
    p_block.set_defaults(fn=cmd_block)

    p_assign = sub.add_parser("assign", help="assign a plan with a context capsule")
    p_assign.add_argument("plan_id")
    p_assign.add_argument("--owner", required=True)
    p_assign.add_argument("--from", dest="from_")
    p_assign.add_argument("--to")
    p_assign.add_argument("--override", action="store_true")
    p_assign.add_argument("--reason")
    p_assign.set_defaults(fn=cmd_assign)

    p_budgets = sub.add_parser("budgets", help="show concurrency budgets and usage")
    p_budgets.set_defaults(fn=cmd_budgets)

    args = parser.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
