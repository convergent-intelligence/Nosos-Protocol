#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            size += len(chunk)
            h.update(chunk)
    return h.hexdigest(), size


def _safe_slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_-]+", "", s)
    return (s[:60] or "proof")


def _merkle_root_hex(leaves_hex: list[str]) -> str:
    if not leaves_hex:
        return ""

    level = [bytes.fromhex(x) for x in leaves_hex]
    while len(level) > 1:
        nxt = []
        it = iter(level)
        for a in it:
            b = next(it, None)
            if b is None:
                b = a
            nxt.append(hashlib.sha256(a + b).digest())
        level = nxt
    return level[0].hex()


def _canonical_json_bytes(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def create_attestation(root: Path, *, title: str, claim: str, evidence_paths: list[str]) -> tuple[Path, dict]:
    out_dir = root / "artifacts" / "proofs"
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = _utc_now_rfc3339()
    date = ts.split("T", 1)[0]
    slug = _safe_slug(title)

    # Normalize evidence into relative paths where possible.
    ev = []
    for p in evidence_paths:
        fp = Path(p).expanduser().resolve()
        if not fp.exists() or not fp.is_file():
            raise SystemExit(f"missing evidence file: {p}")
        digest, size = _sha256_file(fp)
        try:
            rel = str(fp.relative_to(root))
        except Exception:
            rel = str(fp)
        ev.append({"path": rel, "sha256": digest, "size_bytes": size})

    ev.sort(key=lambda e: e["path"])
    leaf_hashes = [hashlib.sha256((e["path"] + ":" + e["sha256"]).encode("utf-8")).hexdigest() for e in ev]
    merkle_root = _merkle_root_hex(leaf_hashes)

    att = {
        "version": "0.1",
        "ts": ts,
        "title": title,
        "claim": claim,
        "evidence": ev,
        "merkle_root": merkle_root,
        "signature": {
            "scheme": "",
            "signer": "",
            "signature": ""
        },
        "onchain": {
            "chain": "",
            "tx_hash": "",
            "anchor": "attestation_hash"
        }
    }

    # Compute attestation hash over canonical bytes of the attestation without signature/onchain filled.
    canonical = _canonical_json_bytes(att)
    att_hash = hashlib.sha256(canonical).hexdigest()
    att["attestation_hash"] = att_hash

    out_path = out_dir / f"{date}_{slug}.json"
    out_path.write_text(json.dumps(att, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_path, att


def verify_attestation(root: Path, att_path: Path) -> dict:
    att = json.loads(att_path.read_text(encoding="utf-8"))
    ev = att.get("evidence") or []
    if not isinstance(ev, list):
        raise SystemExit("invalid attestation: evidence")

    # Recompute evidence hashes.
    recomputed = []
    for e in ev:
        path = str(e.get("path") or "")
        sha = str(e.get("sha256") or "")
        p = (root / path)
        if not p.exists():
            raise SystemExit(f"missing evidence in workspace: {path}")
        digest, size = _sha256_file(p)
        if digest != sha:
            raise SystemExit(f"evidence hash mismatch: {path}")
        recomputed.append({"path": path, "sha256": digest, "size_bytes": size})

    recomputed.sort(key=lambda e: e["path"])
    leaf_hashes = [hashlib.sha256((e["path"] + ":" + e["sha256"]).encode("utf-8")).hexdigest() for e in recomputed]
    merkle_root = _merkle_root_hex(leaf_hashes)
    if merkle_root != str(att.get("merkle_root") or ""):
        raise SystemExit("merkle_root mismatch")

    # Recompute canonical hash.
    tmp = dict(att)
    claimed = str(tmp.pop("attestation_hash", ""))
    canonical = _canonical_json_bytes(tmp)
    computed = hashlib.sha256(canonical).hexdigest()
    if claimed != computed:
        raise SystemExit("attestation_hash mismatch")

    return {"ok": True, "attestation_hash": computed, "merkle_root": merkle_root, "evidence": len(recomputed)}


def cmd_create(args: argparse.Namespace) -> int:
    root = _resolve_root()
    out_path, att = create_attestation(root, title=args.title, claim=args.claim, evidence_paths=list(args.evidence or []))
    print(json.dumps({"path": str(out_path), "attestation_hash": att["attestation_hash"], "merkle_root": att["merkle_root"]}, indent=2, sort_keys=True))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    root = _resolve_root()
    att_path = Path(args.attestation).expanduser().resolve()
    res = verify_attestation(root, att_path)
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="proof")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create")
    c.add_argument("--title", required=True)
    c.add_argument("--claim", required=True)
    c.add_argument("--evidence", action="append", required=True)
    c.set_defaults(fn=cmd_create)

    v = sub.add_parser("verify")
    v.add_argument("--attestation", required=True)
    v.set_defaults(fn=cmd_verify)

    args = ap.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
