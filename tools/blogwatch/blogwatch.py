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
    req = urllib.request.Request(url, headers={"User-Agent": "blogwatch/0.1"})
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


def _find_first(parent: ET.Element, tags: list[str]) -> ET.Element | None:
    for t in tags:
        el = parent.find(t)
        if el is not None:
            return el
    return None


def _parse_rss(root: ET.Element) -> list[dict]:
    ch = root.find("channel")
    if ch is None:
        return []
    out = []
    for it in ch.findall("item"):
        title = _text(it.find("title"))
        link = _text(it.find("link"))
        guid = _text(it.find("guid")) or link
        pub = _text(it.find("pubDate"))
        out.append({"id": guid, "title": title, "link": link, "published": pub})
    return out


def _parse_atom(root: ET.Element) -> list[dict]:
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}", 1)[0] + "}"
    out = []
    for e in root.findall(f"{ns}entry"):
        title = _text(e.find(f"{ns}title"))
        link_el = e.find(f"{ns}link")
        link = _strip(link_el.get("href")) if link_el is not None else ""
        eid = _text(e.find(f"{ns}id")) or link
        pub = _text(_find_first(e, [f"{ns}published", f"{ns}updated"]))
        out.append({"id": eid, "title": title, "link": link, "published": pub})
    return out


def parse_feed(xml_bytes: bytes) -> list[dict]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []

    tag = root.tag.lower()
    if tag.endswith("rss"):
        return _parse_rss(root)
    if tag.endswith("feed"):
        return _parse_atom(root)
    if root.find("channel") is not None:
        return _parse_rss(root)
    return []


@dataclass
class Feed:
    domain: str
    team: str
    id: str
    name: str
    url: str
    tags: list[str]


def _domains_dir(root: Path) -> Path:
    return root / "tools" / "blogwatch" / "domains"


def list_domains(root: Path) -> list[str]:
    d = _domains_dir(root)
    if not d.exists():
        return []
    out = []
    for p in sorted(d.glob("*.json")):
        out.append(p.stem)
    return out


def load_domain(root: Path, domain: str) -> tuple[dict, list[Feed]]:
    p = _domains_dir(root) / f"{domain}.json"
    cfg = _read_json(p)
    feeds: list[Feed] = []
    for team in cfg.get("teams", []):
        team_id = str(team.get("id") or "")
        for f in team.get("feeds", []):
            feeds.append(
                Feed(
                    domain=domain,
                    team=team_id,
                    id=str(f.get("id") or ""),
                    name=str(f.get("name") or ""),
                    url=str(f.get("url") or ""),
                    tags=list(f.get("tags", [])),
                )
            )
    return cfg, feeds


def _state_path(root: Path, domain: str) -> Path:
    return root / "artifacts" / "blogwatch" / domain / "state.json"


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

    base = root / "artifacts" / "blogwatch" / domain
    snap_dir = base / "snapshots"
    entries_path = base / "entries.jsonl"
    now = _utc_now_rfc3339()

    new_count = 0
    err_count = 0

    for f in feeds:
        if not f.url:
            continue
        try:
            data = _http_get(f.url, timeout=timeout)
        except urllib.error.URLError as e:
            err_count += 1
            _append_jsonl(entries_path, {"ts": now, "kind": "error", "domain": domain, "feed": f.id, "error": str(e)})
            continue

        digest = _sha256_bytes(data)
        snap_dir.mkdir(parents=True, exist_ok=True)
        snap_path = snap_dir / f"{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S')}_{f.team}_{f.id}_{digest[:12]}.xml"
        snap_path.write_bytes(data)

        items = parse_feed(data)
        last_seen = str(seen.get(f.id, ""))
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
                "feed": f.id,
                "feed_name": f.name,
                "tags": f.tags,
                "id": item_id,
                "title": it.get("title", ""),
                "link": it.get("link", ""),
                "published": it.get("published", ""),
            }
            _append_jsonl(entries_path, obj)
            new_count += 1
            added += 1
            if added >= max_new_per_feed:
                break

        if items:
            seen[f.id] = str(items[0].get("id") or "")
        time.sleep(sleep_s)

    state["seen"] = seen
    state["last_run_ts"] = now
    save_state(root, domain, state)

    return {"ok": True, "domain": domain, "new": new_count, "errors": err_count, "ts": now, "teams": len(cfg.get('teams', []))}


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
    ap = argparse.ArgumentParser(prog="blogwatch")
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
