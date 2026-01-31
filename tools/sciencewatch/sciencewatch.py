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
    req = urllib.request.Request(url, headers={"User-Agent": "sciencewatch/0.1"})
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
class FeedDef:
    id: str
    name: str
    url: str
    tags: list[str]


def load_feeds(root: Path) -> list[FeedDef]:
    cfg = _read_json(root / "tools" / "sciencewatch" / "feeds.json")
    feeds = []
    for f in cfg.get("feeds", []):
        feeds.append(FeedDef(id=str(f["id"]), name=str(f["name"]), url=str(f["url"]), tags=list(f.get("tags", []))))
    return feeds


def load_state(root: Path) -> dict:
    p = root / "artifacts" / "sciencewatch" / "state.json"
    if not p.exists():
        return {"seen": {}}
    return _read_json(p)


def save_state(root: Path, state: dict) -> None:
    _write_json(root / "artifacts" / "sciencewatch" / "state.json", state)


def cmd_fetch(args: argparse.Namespace) -> int:
    root = _resolve_root()
    feeds = load_feeds(root)
    state = load_state(root)
    seen = state.get("seen", {})

    out_dir = root / "artifacts" / "sciencewatch"
    snap_dir = out_dir / "snapshots"
    entries_path = out_dir / "entries.jsonl"

    now = _utc_now_rfc3339()
    new_count = 0
    err_count = 0

    for f in feeds:
        try:
            data = _http_get(f.url, timeout=int(args.timeout))
        except urllib.error.URLError as e:
            err_count += 1
            _append_jsonl(entries_path, {"ts": now, "kind": "error", "feed": f.id, "error": str(e)})
            continue

        digest = _sha256_bytes(data)
        snap_dir.mkdir(parents=True, exist_ok=True)
        snap_path = snap_dir / f"{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S')}_{f.id}_{digest[:12]}.xml"
        snap_path.write_bytes(data)

        items = parse_feed(data)
        last_seen = str(seen.get(f.id, ""))
        for it in items:
            item_id = str(it.get("id") or "")
            if not item_id:
                continue
            if item_id == last_seen:
                break
            obj = {
                "ts": now,
                "kind": "entry",
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

        if items:
            seen[f.id] = str(items[0].get("id") or "")
        time.sleep(float(args.sleep))

    state["seen"] = seen
    state["last_run_ts"] = now
    save_state(root, state)

    print(json.dumps({"ok": True, "new": new_count, "errors": err_count, "ts": now}, indent=2, sort_keys=True))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    root = _resolve_root()
    feeds = load_feeds(root)
    print(json.dumps([f.__dict__ for f in feeds], indent=2, sort_keys=True))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="sciencewatch")
    sub = ap.add_subparsers(dest="cmd", required=True)

    l = sub.add_parser("list")
    l.set_defaults(fn=cmd_list)

    f = sub.add_parser("fetch")
    f.add_argument("--timeout", default="20")
    f.add_argument("--sleep", default="0.2")
    f.set_defaults(fn=cmd_fetch)

    args = ap.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
