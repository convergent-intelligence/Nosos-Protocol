# Context Capsule: Blockchain proof of discoveries (attestations)

Work ID: PROOF-001
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:55:48Z

## Objective

Deterministic attestations with evidence hashes + merkle root; wallet signature + on-chain anchor later

## Boundaries

In scope:
- Execute this work item exactly as written.
Out of scope:
- Redesign unrelated systems or expand scope without a new item.

## Invariants

- Do not delete originals during automation.
- Blob storage remains content-addressed and immutable.
- Actions remain auditable (append-only log).

## Touch Points

Files linked on the item:
- `docs/web3/proofs.md`
- `scripts/proof`
- `tools/proofs/proof.py`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-055316_proclamation_plan.json`
- `.bridges/signals/20260130-054927_proclamation_plan.json`
- `.bridges/signals/20260130-054416_proclamation_plan.json`
- `.bridges/signals/20260130-053604_proclamation_plan.json`
- `.bridges/signals/20260130-053305_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/web3/proofs.md`

```
# Blockchain Proof of Discoveries

Goal: provide cryptographic, portable proof that a discovery existed at a time, with evidence.

We do this in layers:

Layer 0 (now): local, deterministic attestation
- compute hashes of evidence files
- compute a Merkle root
- compute a canonical attestation hash
- store the attestation in-repo as an artifact

Layer 1 (web3 login): wallet signature
- user signs the attestation hash (or typed data)
- signature is stored with the attestation

Layer 2 (on-chain): anchor
- submit the attestation hash (or Merkle root) to a chain
- store tx hash back in the attestation

## Why This Helps All Substrates

- Any agent can produce an attestation.
- Any verifier can re-hash evidence and confirm the same digest.
- Wallet signature provides accountability without identity disclosure.

## Artifact Format

Attestations live in:
- `artifacts/proofs/`

Each attestation contains:
- claim
- evidence file list with SHA-256
- Merkle root
- canonical attestation hash
- optional wallet signature
- optional on-chain tx hash

## Tooling

- Create an attestation:

```bash
./scripts/proof create --title "TSP exact optimum n=14" --claim "Held-Karp yields optimal tour length 990" \
  --evidence artifacts/math/tsp_n14_seed42.json \
  --evidence artifacts/math/tsp_n14_seed42_exact.json
```

This writes an attestation JSON and prints its hash.
```

### `scripts/proof`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/proofs/proof.py" "$@"
```

### `tools/proofs/proof.py`

```
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

(truncated: 187 lines total)
```

