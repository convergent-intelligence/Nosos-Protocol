#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _safe_slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_-]+", "", s)
    return (s[:60] or "post")


def _parse_front_matter(md: str) -> dict:
    if not md.startswith("---\n"):
        return {}
    end = md.find("\n---\n", 4)
    if end == -1:
        return {}
    block = md[4:end].splitlines()
    out: dict[str, str] = {}
    for line in block:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def cmd_publish(args: argparse.Namespace) -> int:
    root = _resolve_root()
    draft = Path(args.draft).expanduser().resolve()
    if not draft.exists():
        raise SystemExit(f"missing draft: {draft}")

    text = draft.read_text(encoding="utf-8")
    meta = _parse_front_matter(text)
    date = meta.get("date") or dt.datetime.now(dt.timezone.utc).date().isoformat()
    title = meta.get("title") or draft.stem
    slug = _safe_slug(title)

    yyyy, mm, dd = date.split("-")
    out_dir = root / "sites" / "convergent-intelligence" / "posts" / yyyy / mm / dd
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{slug}.md"
    out.write_text(text, encoding="utf-8")

    # Update a simple index.
    idx_path = root / "sites" / "convergent-intelligence" / "posts" / "index.json"
    idx = []
    if idx_path.exists():
        try:
            idx = json.loads(idx_path.read_text(encoding="utf-8"))
        except Exception:
            idx = []
    idx.append({"date": date, "title": title, "path": str(out.relative_to(root))})
    idx_path.write_text(json.dumps(idx, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(str(out))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="publish")
    ap.add_argument("draft")
    args = ap.parse_args(argv)
    return int(cmd_publish(args))


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
