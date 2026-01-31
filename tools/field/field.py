#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _load_table(root: Path) -> dict:
    p = root / "tools" / "field" / "orthogonal-table.json"
    return json.loads(p.read_text(encoding="utf-8"))


def _check_file_exists(root: Path, path: str) -> tuple[bool, str]:
    ok = (root / path).exists()
    return ok, f"file_exists:{path}"


def _check_glob_exists(root: Path, pattern: str) -> tuple[bool, str]:
    matches = list(root.glob(pattern))
    return (len(matches) > 0), f"glob_exists:{pattern}"


def _run_checks(root: Path, element: dict) -> tuple[bool, list[dict]]:
    results: list[dict] = []
    ok_all = True
    for chk in element.get("checks", []):
        kind = chk.get("kind")
        if kind == "file_exists":
            ok, label = _check_file_exists(root, chk.get("path", ""))
        elif kind == "glob_exists":
            ok, label = _check_glob_exists(root, chk.get("pattern", ""))
        else:
            ok = False
            label = f"unknown_check:{kind}"
        results.append({"ok": bool(ok), "check": label})
        ok_all = ok_all and bool(ok)
    return ok_all, results


def compute_field(root: Path) -> dict:
    table = _load_table(root)
    elements = sorted(table.get("elements", []), key=lambda e: int(e.get("z", 0)))
    noble = set(int(x) for x in table.get("noble_gases", []))
    iron = int(table.get("iron_threshold", 26))

    achieved = []
    blocked = None
    z_current = 0
    for e in elements:
        z = int(e.get("z", 0))
        ok, checks = _run_checks(root, e)
        entry = {
            "z": z,
            "symbol": e.get("symbol", ""),
            "name": e.get("name", ""),
            "ok": bool(ok),
            "checks": checks,
            "noble_gas": z in noble,
            "iron_or_beyond": z >= iron,
        }
        if ok and z == z_current + 1:
            z_current = z
            achieved.append(entry)
            continue
        if not ok and blocked is None and z == z_current + 1:
            blocked = entry
        # still record for visibility
        achieved.append(entry)

    next_z = z_current + 1
    next_is_noble = next_z in noble
    return {
        "ts": _utc_now_rfc3339(),
        "z_current": z_current,
        "next_z": next_z,
        "next_is_noble_gas": bool(next_is_noble),
        "blocked": blocked,
        "table_version": table.get("version", ""),
    }


def cmd_status(args: argparse.Namespace) -> int:
    root = _resolve_root()
    field = compute_field(root)
    print(json.dumps(field, indent=2, sort_keys=True))
    return 0


def cmd_write(args: argparse.Namespace) -> int:
    root = _resolve_root()
    field = compute_field(root)
    out = root / ".substrate" / "state" / "field.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(field, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(str(out))
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="field")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="show current field summary")
    s.set_defaults(fn=cmd_status)

    w = sub.add_parser("write", help="write .substrate/state/field.json")
    w.set_defaults(fn=cmd_write)

    args = p.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
