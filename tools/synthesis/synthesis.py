#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def _utc_now_rfc3339() -> str:
    return _utc_now().isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _run_json(root: Path, rel_cmd: list[str]) -> Any:
    cmd = [str(root / rel_cmd[0]), *rel_cmd[1:]]
    cp = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(cp.stdout)


def _count_recent_files(dir_path: Path, *, since: dt.datetime) -> int:
    if not dir_path.exists():
        return 0
    n = 0
    for p in dir_path.glob("*"):
        try:
            if dt.datetime.fromtimestamp(p.stat().st_mtime, tz=dt.timezone.utc) >= since:
                n += 1
        except Exception:
            continue
    return n


def _signals_summary(root: Path, limit: int) -> tuple[dict, list[str]]:
    sig_dir = root / ".bridges" / "signals"
    if not sig_dir.exists():
        return {"total": 0, "by_kind": {}}, []
    paths = sorted(sig_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    by_kind: dict[str, int] = {}
    last: list[str] = []
    for p in paths[:limit]:
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
            kind = str((obj.get("header") or {}).get("kind") or "")
            if kind:
                by_kind[kind] = by_kind.get(kind, 0) + 1
        except Exception:
            pass
        last.append(str(p.relative_to(root)))
    return {"total": len(paths), "by_kind": by_kind}, last


def compute(root: Path) -> dict:
    now = _utc_now()
    since_24h = now - dt.timedelta(hours=24)

    budgets_obj = _run_json(root, ["scripts/orchestrate", "budgets"])
    field_obj = _run_json(root, ["scripts/field", "status"])
    health_obj = _run_json(root, ["scripts/health.sh"])

    budgets = cast(dict, budgets_obj) if isinstance(budgets_obj, dict) else {}
    field = cast(dict, field_obj) if isinstance(field_obj, dict) else {}
    health = cast(dict, health_obj) if isinstance(health_obj, dict) else {}

    active = _run_json(root, ["scripts/orchestrate", "active", "--json"])
    next_items = _run_json(root, ["scripts/orchestrate", "next", "--json"])

    leases_dir = root / ".substrate" / "state" / "leases"
    leases = []
    for p in leases_dir.glob("*.json"):
        try:
            leases.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue

    contexts_24h = _count_recent_files(root / "artifacts" / "contexts", since=since_24h)

    sig_summary, last_signals = _signals_summary(root, limit=12)

    active_list = active if isinstance(active, list) else []
    next_list = next_items if isinstance(next_items, list) else []

    out = {
        "ts": _utc_now_rfc3339(),
        "field": field,
        "health": {
            "health": health.get("health"),
            "inbox_failed": health.get("inbox_failed"),
            "autofile": health.get("autofile"),
        },
        "budgets": budgets,
        "active": active_list,
        "next": next_list[:10],
        "leases": {
            "count": len(leases),
            "items": leases,
        },
        "signals": {
            "summary": sig_summary,
            "recent": last_signals,
        },
        "drift": {
            "capsules_created_last_24h": contexts_24h,
        },
    }
    return out


def render_md(summary: dict) -> str:
    field = summary.get("field") or {}
    health = summary.get("health") or {}
    budgets = summary.get("budgets") or {}
    drift = summary.get("drift") or {}
    signals = summary.get("signals") or {}

    lines: list[str] = []
    lines.append(f"# Synthesis Report ({summary.get('ts','')})")
    lines.append("")
    lines.append("## Field")
    lines.append(f"- z_current: {field.get('z_current')} (next: {field.get('next_z')})")
    lines.append(f"- next_is_noble_gas: {field.get('next_is_noble_gas')}")
    lines.append("")
    lines.append("## Health")
    lines.append(f"- health: {health.get('health')}")
    lines.append(f"- inbox_failed: {health.get('inbox_failed')}")
    af = health.get("autofile") or {}
    lines.append(f"- autofile: blobs={af.get('blobs')} units={af.get('units')} quarantined_units={af.get('quarantined_units')}")
    lines.append("")
    lines.append("## Budgets")
    b = budgets.get("budgets") or {}
    ip = budgets.get("in_progress_by_domain") or {}
    lines.append(f"- max_in_progress_per_domain: {b.get('max_in_progress_per_domain')}")
    lines.append(f"- in_progress_by_domain: {ip}")
    lines.append("")
    lines.append("## Drift")
    lines.append(f"- capsules_created_last_24h: {drift.get('capsules_created_last_24h')}")
    lines.append("")
    lines.append("## Signals")
    ss = (signals.get("summary") or {}).get("by_kind") or {}
    lines.append(f"- by_kind_recent12: {ss}")
    for p in (signals.get("recent") or []):
        lines.append(f"- `{p}`")
    lines.append("")
    lines.append("## Active")
    for item in summary.get("active") or []:
        lines.append(f"- {item.get('id')} {item.get('title')} ({item.get('domain')}/{item.get('priority')})")
    lines.append("")
    lines.append("## Next")
    for item in summary.get("next") or []:
        lines.append(f"- {item.get('id')} {item.get('title')} ({item.get('domain')}/{item.get('priority')})")
    lines.append("")
    return "\n".join(lines)


def cmd_run(args: argparse.Namespace) -> int:
    root = _resolve_root()
    summary = compute(root)

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    out_dir = root / ".synthesis" / "consensus"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    md_path = out_dir / f"{ts}.md"
    md_path.write_text(render_md(summary) + "\n", encoding="utf-8")

    corr_dir = root / ".synthesis" / "correlations"
    corr_dir.mkdir(parents=True, exist_ok=True)
    (corr_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(str(md_path))
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="synthesize")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_run)
    args = p.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
