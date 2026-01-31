#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _safe_slug(s: str) -> str:
    s = s.strip().lower().replace(" ", "-")
    s = "".join(ch for ch in s if ch.isalnum() or ch in ("-", "_"))
    return (s[:60] or "item")


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_yaml_list_of_maps(text: str, list_key: str) -> list[dict]:
    lines = text.splitlines()
    in_list = False
    items: list[dict] = []
    cur: dict | None = None
    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        s = raw.strip()
        i += 1
        if not s or s.startswith("#"):
            continue
        if not in_list:
            if s == f"{list_key}:":
                in_list = True
            continue

        if s.startswith("-") and ":" in s:
            if cur is not None:
                items.append(cur)
            cur = {}
            after = s[1:].strip()
            k, v = after.split(":", 1)
            cur[k.strip()] = _strip_quotes(v.strip())
            continue

        if cur is None:
            continue

        if s == "links:" or s == "depends_on:":
            key = s[:-1]
            cur.setdefault(key, [])
            while i < len(lines):
                nxt = lines[i].rstrip("\n")
                ns = nxt.strip()
                if not ns or ns.startswith("#"):
                    i += 1
                    continue
                if not ns.startswith("-"):
                    break
                cur[key].append(_strip_quotes(ns[1:].strip()))
                i += 1
            continue

        if ":" in s:
            k, v = s.split(":", 1)
            cur[k.strip()] = _strip_quotes(v.strip())

    if cur is not None:
        items.append(cur)
    return items


@dataclass(frozen=True)
class WorkItem:
    id: str
    title: str
    kind: str
    status: str
    owner: str
    domain: str
    priority: str
    links: list[str]
    depends_on: list[str]
    notes: str


def load_item(root: Path, item_id: str) -> WorkItem:
    path = root / "tools" / "plan-registry" / "plans.yaml"
    items = parse_yaml_list_of_maps(_read(path), "plans")
    for it in items:
        if str(it.get("id", "")) != item_id:
            continue
        return WorkItem(
            id=item_id,
            title=str(it.get("title", "")),
            kind=str(it.get("kind", "plan")),
            status=str(it.get("status", "pending")),
            owner=str(it.get("owner", "unassigned")),
            domain=str(it.get("domain", "unassigned")),
            priority=str(it.get("priority", "medium")),
            links=list(it.get("links", []) or []),
            depends_on=list(it.get("depends_on", []) or []),
            notes=str(it.get("notes", "")),
        )
    raise SystemExit(f"unknown work item: {item_id}")


def _read_health(root: Path) -> dict | None:
    p = root / ".substrate" / "state" / "health.json"
    if not p.exists():
        return None
    try:
        return json.loads(_read(p))
    except Exception:
        return None


def _recent_signals(root: Path, limit: int) -> list[str]:
    sig_dir = root / ".bridges" / "signals"
    if not sig_dir.exists():
        return []
    paths = sorted(sig_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p.relative_to(root)) for p in paths[:limit]]


def _embed_file(root: Path, rel: str, *, max_lines: int) -> str:
    p = (root / rel).resolve()
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return f"(unable to read {rel})\n"
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text.rstrip() + "\n"
    head = "\n".join(lines[:max_lines])
    return head.rstrip() + f"\n\n(truncated: {len(lines)} lines total)\n"


def _update_plan_links_add(root: Path, item_id: str, new_link: str) -> None:
    """Append a link to the target item's links list, if missing.

    Best-effort text edit; assumes links are either `links: []` or a `links:` block.
    """

    path = root / "tools" / "plan-registry" / "plans.yaml"
    lines = _read(path).splitlines(True)

    # Locate item.
    start = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not (s.startswith("-") and "id:" in s):
            continue
        after = s[1:].strip()
        try:
            k, v = after.split(":", 1)
        except Exception:
            continue
        if k.strip() != "id":
            continue
        if _strip_quotes(v.strip()) == item_id:
            start = i
            break
    if start is None:
        return

    end = len(lines)
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if s.startswith("-") and "id:" in s:
            end = j
            break

    item = lines[start:end]
    base_indent = " " * (len(item[0]) - len(item[0].lstrip(" ")) + 2)
    link_indent = base_indent + "  "

    # If link already present, no-op.
    for ln in item:
        if ln.strip() == f"- \"{new_link}\"" or ln.strip() == f"- '{new_link}'" or ln.strip() == f"- {new_link}":
            return

    # Find links block.
    for idx, ln in enumerate(item):
        if ln.strip() == "links: []":
            item[idx] = f"{base_indent}links:\n"
            item[idx + 1:idx + 1] = [f"{link_indent}- \"{new_link}\"\n"]
            lines[start:end] = item
            _write(path, "".join(lines))
            return

        if ln.strip() == "links:":
            # Insert after existing link lines.
            insert_at = idx + 1
            while insert_at < len(item) and item[insert_at].strip().startswith("-"):
                insert_at += 1
            item[insert_at:insert_at] = [f"{link_indent}- \"{new_link}\"\n"]
            lines[start:end] = item
            _write(path, "".join(lines))
            return

    # No links key found; add after title.
    insert_at = 1
    for idx, ln in enumerate(item):
        if ln.strip().startswith("title:"):
            insert_at = idx + 1
            break
    item[insert_at:insert_at] = [f"{base_indent}links:\n", f"{link_indent}- \"{new_link}\"\n"]
    lines[start:end] = item
    _write(path, "".join(lines))


def build_capsule(root: Path, item: WorkItem, *, max_files: int, max_lines: int, recent_signal_limit: int) -> Path:
    out_dir = root / "artifacts" / "contexts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{item.id}_{_safe_slug(item.title)}.md"

    health = _read_health(root)
    signals = _recent_signals(root, recent_signal_limit)

    # Exclude other capsules from the capsule itself (avoid recursion).
    effective_links = [l for l in item.links if not l.startswith("artifacts/contexts/")]

    # Choose which linked files to embed: only existing, non-binary, and limited.
    embed = []
    for rel in effective_links:
        p = root / rel
        if p.is_dir():
            continue
        if not p.exists():
            continue
        # Skip obvious binaries by extension.
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".tar"}:
            continue
        embed.append(rel)
        if len(embed) >= max_files:
            break

    parts = []
    parts.append(f"# Context Capsule: {item.title}\n\n")
    parts.append(f"Work ID: {item.id}\n")
    parts.append(f"Kind: {item.kind}\n")
    parts.append(f"Domain: {item.domain}\n")
    parts.append(f"Priority: {item.priority}\n")
    parts.append(f"Status: {item.status}\n")
    parts.append(f"Owner: {item.owner}\n")
    parts.append(f"Generated: {_utc_now_rfc3339()}\n\n")

    parts.append("## Objective\n\n")
    parts.append((item.notes or "").strip() + "\n\n")

    parts.append("## Boundaries\n\n")
    parts.append("In scope:\n- Execute this work item exactly as written.\n")
    parts.append("Out of scope:\n- Redesign unrelated systems or expand scope without a new item.\n\n")

    parts.append("## Invariants\n\n")
    parts.append("- Do not delete originals during automation.\n")
    parts.append("- Blob storage remains content-addressed and immutable.\n")
    parts.append("- Actions remain auditable (append-only log).\n\n")

    parts.append("## Touch Points\n\n")
    parts.append("Files linked on the item:\n")
    if effective_links:
        for l in effective_links:
            parts.append(f"- `{l}`\n")
    else:
        parts.append("- (none)\n")
    parts.append("\nCommands:\n\n```bash\n./scripts/validate.sh\n./scripts/health.sh\n```\n\n")

    parts.append("## Current State\n\n")
    if health is None:
        parts.append("- Health: (no health snapshot yet)\n")
    else:
        parts.append(f"- Health: {health.get('health','')}\n")
        af = health.get("autofile") or {}
        parts.append(f"- AutoFile: blobs={af.get('blobs')} units={af.get('units')} quarantined_units={af.get('quarantined_units')}\n")
    parts.append("\nRecent signals:\n")
    if signals:
        for s in signals:
            parts.append(f"- `{s}`\n")
    else:
        parts.append("- (none)\n")
    parts.append("\n")

    parts.append("## Drift Guards\n\n")
    parts.append("- Do not pull in extra context unless the capsule says so.\n")
    parts.append("- If you need more than 5 files, stop and create a stub explaining why.\n")
    parts.append("- If the task is ambiguous, stop and emit a council_call signal.\n\n")

    if embed:
        parts.append("## Embedded Context\n\n")
        for rel in embed:
            parts.append(f"### `{rel}`\n\n")
            parts.append("```\n")
            parts.append(_embed_file(root, rel, max_lines=max_lines))
            parts.append("```\n\n")

    _write(out, "".join(parts))
    return out


def cmd_make(args: argparse.Namespace) -> int:
    root = _resolve_root()
    item = load_item(root, args.work_id)
    capsule = build_capsule(root, item, max_files=int(args.max_files), max_lines=int(args.max_lines), recent_signal_limit=int(args.signals))
    rel = str(capsule.relative_to(root))
    _update_plan_links_add(root, item.id, rel)
    print(str(capsule))
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="context")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("make", help="generate a context capsule for a work item")
    m.add_argument("work_id")
    m.add_argument("--max-files", default="5")
    m.add_argument("--max-lines", default="120")
    m.add_argument("--signals", default="5")
    m.set_defaults(fn=cmd_make)

    args = p.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
