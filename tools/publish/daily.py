#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path


def _utc_today() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


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


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _read_last_entries(entries_path: Path, limit: int) -> list[dict]:
    if not entries_path.exists():
        return []
    lines = entries_path.read_text(encoding="utf-8").splitlines()
    out: list[dict] = []
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if obj.get("kind") != "entry":
            continue
        out.append(obj)
        if len(out) >= limit:
            break
    out.reverse()
    return out


def _draft_path(root: Path, date: str, domain: str) -> Path:
    slug = _safe_slug(domain)
    return root / "sites" / "convergent-intelligence" / "drafts" / f"{date}_{slug}.md"


def cmd_create(args: argparse.Namespace) -> int:
    root = _resolve_root()
    date = args.date or _utc_today()
    domain = args.domain

    draft = _draft_path(root, date, domain)
    if draft.exists() and not args.force:
        print(str(draft))
        return 0

    # Fetch sources (best-effort).
    if not args.no_fetch:
        _run([str(root / "scripts" / "blogwatch"), "fetch", "--domain", domain, "--max-new-per-feed", str(args.max_new_per_feed)])

    entries_path = root / "artifacts" / "blogwatch" / domain / "entries.jsonl"
    entries = _read_last_entries(entries_path, limit=int(args.sources))

    # Create a bounded draft template.
    lines: list[str] = []
    lines.append("---")
    lines.append(f"date: {date}")
    lines.append(f"domain: {domain}")
    lines.append("title: \"\"")
    lines.append("status: draft")
    lines.append("confidence: 0.6")
    lines.append("expected_impact: medium")
    lines.append("measurement: \"What would change the confidence?\"")
    lines.append("evidence:")
    lines.append(f"  - artifacts/blogwatch/{domain}/entries.jsonl")
    lines.append("---")
    lines.append("")
    lines.append("# ")
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append("## Why This Matters")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")
    lines.append("## Reproduce")
    lines.append("")
    lines.append("```bash")
    lines.append(f"./scripts/blogwatch fetch --domain {domain}")
    lines.append("```")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    if entries:
        for e in entries:
            title = str(e.get("title") or "").strip()
            link = str(e.get("link") or "").strip()
            feed = str(e.get("feed") or "")
            team = str(e.get("team") or "")
            if title and link:
                lines.append(f"- [{title}]({link}) ({domain}/{team}/{feed})")
    else:
        lines.append("- (no sources captured yet)")

    draft.parent.mkdir(parents=True, exist_ok=True)
    draft.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Record a daily release artifact.
    rec_dir = root / "artifacts" / "publish" / "daily"
    rec_dir.mkdir(parents=True, exist_ok=True)
    rec = {
        "ts": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "date": date,
        "domain": domain,
        "draft": str(draft.relative_to(root)),
        "sources_count": len(entries),
    }
    (rec_dir / f"{date}_{_safe_slug(domain)}.json").write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(str(draft))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="daily")
    ap.add_argument("--domain", required=True)
    ap.add_argument("--date")
    ap.add_argument("--sources", default="10")
    ap.add_argument("--max-new-per-feed", default="25")
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    return int(cmd_create(args))


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
