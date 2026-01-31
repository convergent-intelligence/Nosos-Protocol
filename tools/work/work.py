#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
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


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _exists_id(plans_text: str, work_id: str) -> bool:
    needle = f"- id: \"{work_id}\""
    return needle in plans_text


def _append_item(
    root: Path,
    *,
    kind: str,
    work_id: str,
    title: str,
    domain: str,
    priority: str,
    owner: str,
    mode: str,
    notes: str,
    links: list[str],
    depends_on: list[str],
) -> None:
    path = root / "tools" / "plan-registry" / "plans.yaml"
    text = _read(path)
    if _exists_id(text, work_id):
        raise SystemExit(f"id already exists: {work_id}")

    block = []
    block.append("\n")
    block.append(f"  - id: \"{work_id}\"\n")
    block.append(f"    title: \"{title}\"\n")
    block.append(f"    kind: \"{kind}\"\n")
    block.append(f"    mode: \"{mode}\"\n")
    block.append("    status: \"pending\"\n")
    block.append(f"    owner: \"{owner}\"\n")
    block.append(f"    domain: \"{domain}\"\n")
    block.append(f"    priority: \"{priority}\"\n")
    if links:
        block.append("    links:\n")
        for l in links:
            block.append(f"      - \"{l}\"\n")
    else:
        block.append("    links: []\n")
    if depends_on:
        block.append("    depends_on:\n")
        for d in depends_on:
            block.append(f"      - \"{d}\"\n")
    else:
        block.append("    depends_on: []\n")
    block.append(f"    notes: \"{notes}\"\n")

    if not text.endswith("\n"):
        text += "\n"
    _write(path, text + "".join(block))


def _create_template(root: Path, kind: str, work_id: str, title: str) -> Path:
    ts = _utc_now_rfc3339()
    safe = title.strip().lower().replace(" ", "-")
    safe = "".join(ch for ch in safe if ch.isalnum() or ch in ("-", "_"))[:60] or "item"

    if kind in ("bug", "issue"):
        out_dir = root / "artifacts" / "issues"
        template = root / "docs" / "templates" / ("bug.md" if kind == "bug" else "issue.md")
    else:
        out_dir = root / "artifacts" / "stubs"
        template = root / "docs" / "templates" / ("dead-end.md" if kind == "dead_end" else "stub.md")

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{work_id}_{safe}.md"
    body = _read(template)
    body = body.replace("<title>", title).replace("<work id>", work_id)
    body = body.replace("2026-01-30", ts.split("T")[0])
    out.write_text(body + "\n", encoding="utf-8")
    return out


def cmd_new(args: argparse.Namespace) -> int:
    root = _resolve_root()
    links = list(args.link or [])
    depends_on = list(args.depends_on or [])
    notes = args.notes or ""

    template_path = None
    if args.template:
        template_path = _create_template(root, args.kind, args.id, args.title)
        links.append(str(template_path.relative_to(root)))

    _append_item(
        root,
        kind=args.kind,
        work_id=args.id,
        title=args.title,
        domain=args.domain,
        priority=args.priority,
        owner=args.owner,
        mode=args.mode,
        notes=notes,
        links=links,
        depends_on=depends_on,
    )

    if template_path is not None:
        print(str(template_path))
    else:
        print(args.id)
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="work")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="create a new work item")
    p_new.add_argument("kind", choices=["plan", "issue", "bug", "dead_end", "stub"])
    p_new.add_argument("id")
    p_new.add_argument("title")
    p_new.add_argument("--domain", default="unassigned", choices=["watcher", "builder", "guardian", "scribe", "gems", "unassigned"])
    p_new.add_argument("--priority", default="medium", choices=["high", "medium", "low"])
    p_new.add_argument("--owner", default="unassigned")
    p_new.add_argument("--mode", default="phase", choices=["phase", "revolution"])
    p_new.add_argument("--notes")
    p_new.add_argument("--link", action="append")
    p_new.add_argument("--depends-on", dest="depends_on", action="append")
    p_new.add_argument("--template", action="store_true")
    p_new.set_defaults(fn=cmd_new)

    args = parser.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
