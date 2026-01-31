#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _run_json(root: Path, rel: list[str]) -> Any:
    cmd = [str(root / rel[0]), *rel[1:]]
    cp = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(cp.stdout)


def _write_focus(root: Path, obj: dict) -> Path:
    out = root / ".substrate" / "state" / "focus.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def _load_levels(root: Path) -> dict:
    p = root / "tools" / "focus" / "levels.json"
    if not p.exists():
        return {"default_level": 2, "levels": {"2": {"name": "operate", "weights": {}}}}
    return json.loads(p.read_text(encoding="utf-8"))


def _resolve_level(root: Path, arg_level: int | None) -> int:
    if arg_level is not None:
        return int(arg_level)
    env = os.environ.get("ASF_FOCUS_LEVEL")
    if env:
        try:
            return int(env)
        except Exception:
            return 2
    levels = _load_levels(root)
    return int(levels.get("default_level") or 2)


def compute_focus(root: Path, *, level: int) -> dict:
    # Update health and field state as part of the ritual.
    health = _run_json(root, ["scripts/health.sh"])
    _ = subprocess.run([str(root / "scripts/field"), "write"], check=True, capture_output=True, text=True)
    field = _run_json(root, ["scripts/field", "status"])
    budgets = _run_json(root, ["scripts/orchestrate", "budgets"])
    active = _run_json(root, ["scripts/orchestrate", "active", "--json"])
    nxt = _run_json(root, ["scripts/orchestrate", "next", "--json"])

    z = int((field or {}).get("z_current") or 0)
    interesting = {10: "closed_shell", 12: "ignition", 17: "purification"}
    flags = {"z_is_interesting": z in interesting, "z_label": interesting.get(z, "")}

    levels = _load_levels(root)
    preset = (levels.get("levels") or {}).get(str(level)) or {}

    return {
        "ts": _utc_now_rfc3339(),
        "focus_level": level,
        "focus_mode": preset.get("name", ""),
        "weights": preset.get("weights", {}),
        "intent": preset.get("intent", ""),
        "rituals": preset.get("rituals", []),
        "field": field,
        "health": health,
        "budgets": budgets,
        "active": active if isinstance(active, list) else [],
        "next": (nxt[:10] if isinstance(nxt, list) else []),
        "flags": flags,
    }


def cmd_status(args: argparse.Namespace) -> int:
    root = _resolve_root()
    level = _resolve_level(root, getattr(args, "level", None))
    focus = compute_focus(root, level=level)
    out = _write_focus(root, focus)

    if args.json:
        print(json.dumps(focus, indent=2, sort_keys=True))
        return 0

    field = focus.get("field") or {}
    health = focus.get("health") or {}
    flags = focus.get("flags") or {}
    z = field.get("z_current")
    label = flags.get("z_label")
    suffix = f" ({label})" if label else ""
    mode = focus.get("focus_mode") or ""
    mode_s = f" {mode}" if mode else ""
    print(f"focus: L{level}{mode_s} z={z}{suffix} health={health.get('health')} active={len(focus.get('active') or [])} -> {out}")
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    root = _resolve_root()
    level = _resolve_level(root, getattr(args, "level", None))
    focus = compute_focus(root, level=level)
    _ = _write_focus(root, focus)

    field = focus.get("field") or {}
    health = focus.get("health") or {}
    budgets = focus.get("budgets") or {}
    active = focus.get("active") or []
    nxt = focus.get("next") or []

    z = field.get("z_current")
    next_z = field.get("next_z")

    lines: list[str] = []
    mode = focus.get("focus_mode") or ""
    mode_s = f" {mode}" if mode else ""
    lines.append(f"route: L{level}{mode_s} z={z} next_z={next_z} health={health.get('health')}")

    intent = str(focus.get("intent") or "")

    # L1/L5: always prefer repair/verify.
    if health.get("health") == "red" or int(health.get("inbox_failed") or 0) > 0:
        lines.append("- priority: repair")
        lines.append("- action: inspect inbox failures and unblock ingestion")
        lines.append("- command: ./scripts/health.sh")
        lines.append("- command: ls -la inbox/failed")
        print("\n".join(lines))
        return 0

    # Finish active items before starting new ones.
    if len(active) > 0:
        lines.append("- priority: finish active")
        for it in active[:3]:
            lines.append(f"- active: {it.get('id')} {it.get('title')}")
        print("\n".join(lines))
        return 0

    # Otherwise, pick the next action based on intent.
    if intent == "ship":
        lines.append("- priority: ship")
        lines.append("- action: build and verify distro")
        lines.append("- command: ./scripts/build-distro.sh")
        lines.append("- command: ./scripts/verify-distro.sh")
        print("\n".join(lines))
        return 0

    if intent == "stabilize":
        lines.append("- priority: stabilize")
        lines.append("- action: run synthesis and review signals")
        lines.append("- command: ./scripts/synthesize")
        lines.append("- command: ls -la .bridges/signals")
        print("\n".join(lines))
        return 0

    lines.append("- priority: start one new item")
    lines.append(f"- budgets: {budgets.get('in_progress_by_domain')}")
    if not nxt:
        lines.append("- next: (none pending)")
        lines.append("- hint: create one with ./scripts/work new plan <ID> \"<title>\"")
    else:
        for it in nxt[:3]:
            lines.append(f"- next: {it.get('id')} {it.get('title')} ({it.get('domain')}/{it.get('priority')})")
            lines.append(f"- assign: ./scripts/orchestrate assign {it.get('id')} --owner <owner>")

    print("\n".join(lines))
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    root = _resolve_root()
    level = _resolve_level(root, getattr(args, "level", None))
    levels = _load_levels(root)
    preset = (levels.get("levels") or {}).get(str(level)) or {}

    out = {
        "level": level,
        "name": preset.get("name", ""),
        "intent": preset.get("intent", ""),
        "weights": preset.get("weights", {}),
        "rituals": preset.get("rituals", []),
    }

    if args.json:
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    print(f"level {level}: {out['name']} intent={out['intent']}")
    print(f"weights: {out['weights']}")
    if out["rituals"]:
        print("rituals:")
        for r in out["rituals"]:
            print(f"- {r}")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="focus")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("status", help="write focus.json and print summary")
    s.add_argument("--json", action="store_true")
    s.add_argument("--level", type=int)
    s.set_defaults(fn=cmd_status)

    r = sub.add_parser("route", help="suggest the next safe action")
    r.add_argument("--level", type=int)
    r.set_defaults(fn=cmd_route)

    e = sub.add_parser("explain", help="explain a focus level preset")
    e.add_argument("--level", type=int)
    e.add_argument("--json", action="store_true")
    e.set_defaults(fn=cmd_explain)

    # Back-compat: `focus --json` and `focus` act like `focus status`.
    if argv and argv[0] == "--json":
        argv = ["status", "--json"]
    elif not argv:
        argv = ["status"]

    args = p.parse_args(argv)
    if not getattr(args, "fn", None):
        args = p.parse_args(["status", *argv])
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
