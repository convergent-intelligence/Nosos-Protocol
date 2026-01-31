#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def append_event(root: Path, event: dict) -> Path:
    p = root / "artifacts" / "rewards" / "ledger.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")
    return p


def cmd_award(args: argparse.Namespace) -> int:
    root = _resolve_root()
    event = {
        "ts": _utc_now_rfc3339(),
        "actor": args.actor,
        "action": args.action,
        "ref": args.ref or "",
        "points": int(args.points),
        "evidence": list(args.evidence or []),
        "notes": args.notes or "",
    }
    p = append_event(root, event)
    print(str(p))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="reward")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("award", help="append a reward event")
    a.add_argument("--actor", required=True)
    a.add_argument("--action", required=True)
    a.add_argument("--points", required=True)
    a.add_argument("--ref")
    a.add_argument("--evidence", action="append")
    a.add_argument("--notes")
    a.set_defaults(fn=cmd_award)

    args = ap.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
