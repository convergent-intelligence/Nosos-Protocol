#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def _utc_now_rfc3339() -> str:
    return _utc_now().isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")


def _http_get(url: str, *, timeout: int) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "githubwatch/0.1",
            "Accept": "application/atom+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.1",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _strip(s: str | None) -> str:
    return (s or "").strip()


def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return _strip(el.text)


def _parse_atom(xml_bytes: bytes) -> list[dict]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []

    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}", 1)[0] + "}"

    out = []
    for e in root.findall(f"{ns}entry"):
        title = _text(e.find(f"{ns}title"))
        link_el = e.find(f"{ns}link")
        link = _strip(link_el.get("href")) if link_el is not None else ""
        eid = _text(e.find(f"{ns}id")) or link
        updated = _text(e.find(f"{ns}updated"))
        out.append({"id": eid, "title": title, "link": link, "updated": updated})
    return out


@dataclass
class RepoFeed:
    repo: str
    team: str
    stream: str
    url: str
    tags: list[str]


def _domains_dir(root: Path) -> Path:
    return root / "tools" / "githubwatch" / "domains"


def list_domains(root: Path) -> list[str]:
    d = _domains_dir(root)
    if not d.exists():
        return []
    return sorted([p.stem for p in d.glob("*.json")])


def load_domain(root: Path, domain: str) -> tuple[dict, list[RepoFeed]]:
    cfg_path = _domains_dir(root) / f"{domain}.json"
    cfg = _read_json(cfg_path)
    feeds: list[RepoFeed] = []
    for team in cfg.get("teams", []):
        team_id = str(team.get("id") or "")
        team_tags = list(team.get("tags", []))
        for repo in team.get("repos", []):
            r = str(repo.get("repo") or "")
            streams = list(repo.get("streams", []))
            branch = str(repo.get("branch") or "main")
            tags = team_tags + list(repo.get("tags", []))
            for stream in streams:
                if stream == "releases":
                    url = f"https://github.com/{r}/releases.atom"
                elif stream == "issues":
                    url = f"https://github.com/{r}/issues.atom"
                elif stream == "pulls":
                    url = f"https://github.com/{r}/pulls.atom"
                elif stream == "commits":
                    url = f"https://github.com/{r}/commits/{branch}.atom"
                else:
                    continue
                feeds.append(RepoFeed(repo=r, team=team_id, stream=stream, url=url, tags=tags))
    return cfg, feeds


def _state_path(root: Path, domain: str) -> Path:
    return root / "artifacts" / "githubwatch" / domain / "state.json"


def load_state(root: Path, domain: str) -> dict:
    p = _state_path(root, domain)
    if not p.exists():
        return {"seen": {}}
    return _read_json(p)


def save_state(root: Path, domain: str, state: dict) -> None:
    _write_json(_state_path(root, domain), state)


def fetch_domain(root: Path, domain: str, *, timeout: int, sleep_s: float, max_new_per_feed: int) -> dict:
    cfg, feeds = load_domain(root, domain)
    state = load_state(root, domain)
    seen = state.get("seen", {})

    base = root / "artifacts" / "githubwatch" / domain
    snap_dir = base / "snapshots"
    entries_path = base / "entries.jsonl"
    now = _utc_now_rfc3339()

    new_count = 0
    err_count = 0

    for f in feeds:
        key = f"{f.repo}:{f.stream}"
        last_seen = str(seen.get(key, ""))
        try:
            data = _http_get(f.url, timeout=timeout)
        except urllib.error.URLError as e:
            err_count += 1
            _append_jsonl(entries_path, {"ts": now, "kind": "error", "domain": domain, "repo": f.repo, "stream": f.stream, "error": str(e)})
            continue

        digest = _sha256_bytes(data)
        snap_dir.mkdir(parents=True, exist_ok=True)
        snap_path = snap_dir / f"{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S')}_{f.team}_{f.repo.replace('/', '_')}_{f.stream}_{digest[:12]}.xml"
        snap_path.write_bytes(data)

        items = _parse_atom(data)
        added = 0
        for it in items:
            item_id = str(it.get("id") or "")
            if not item_id:
                continue
            if item_id == last_seen:
                break
            obj = {
                "ts": now,
                "kind": "entry",
                "domain": domain,
                "team": f.team,
                "repo": f.repo,
                "stream": f.stream,
                "tags": f.tags,
                "id": item_id,
                "title": it.get("title", ""),
                "link": it.get("link", ""),
                "updated": it.get("updated", ""),
            }
            _append_jsonl(entries_path, obj)
            new_count += 1
            added += 1
            if added >= max_new_per_feed:
                break

        if items:
            seen[key] = str(items[0].get("id") or "")
        time.sleep(sleep_s)

    state["seen"] = seen
    state["last_run_ts"] = now
    save_state(root, domain, state)

    return {"ok": True, "domain": domain, "new": new_count, "errors": err_count, "ts": now, "teams": len(cfg.get('teams', [])), "feeds": len(feeds)}


def cmd_domains(args: argparse.Namespace) -> int:
    root = _resolve_root()
    print(json.dumps(list_domains(root), indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    root = _resolve_root()
    cfg, feeds = load_domain(root, args.domain)
    out = {
        "domain": cfg.get("domain"),
        "name": cfg.get("name"),
        "description": cfg.get("description"),
        "teams": cfg.get("teams", []),
        "feed_count": len(feeds),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    root = _resolve_root()
    timeout = int(args.timeout)
    sleep_s = float(args.sleep)
    max_new = int(args.max_new_per_feed)

    results = []
    if args.all:
        for d in list_domains(root):
            results.append(fetch_domain(root, d, timeout=timeout, sleep_s=sleep_s, max_new_per_feed=max_new))
    else:
        results.append(fetch_domain(root, args.domain, timeout=timeout, sleep_s=sleep_s, max_new_per_feed=max_new))
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="githubwatch")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("domains")
    d.set_defaults(fn=cmd_domains)

    l = sub.add_parser("list")
    l.add_argument("--domain", required=True)
    l.set_defaults(fn=cmd_list)

    f = sub.add_parser("fetch")
    f.add_argument("--domain")
    f.add_argument("--all", action="store_true")
    f.add_argument("--timeout", default="20")
    f.add_argument("--sleep", default="0.2")
    f.add_argument("--max-new-per-feed", default="50")
    f.set_defaults(fn=cmd_fetch)

    args = ap.parse_args(argv)
    if args.cmd == "fetch" and not args.all and not args.domain:
        raise SystemExit("provide --domain or --all")
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
