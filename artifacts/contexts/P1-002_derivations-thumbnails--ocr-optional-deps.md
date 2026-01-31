# Context Capsule: Derivations: thumbnails + OCR (optional deps)

Work ID: P1-002
Kind: plan
Domain: scribe
Priority: medium
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:02:46Z

## Objective

Idempotent derived artifacts keyed by blob hash

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
- `docs/roadmap-systems-engineering.md`
- `store/derived/`
- `tools/autofile/autofile.py`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=2 units=3 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-040219_missive_assignment.json`
- `.bridges/signals/20260130-035938_missive_assignment.json`
- `.bridges/signals/20260130-035836_proclamation_plan.json`
- `.bridges/signals/20260130-035647_missive_assignment.json`
- `.bridges/signals/20260130-035536_missive_assignment.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/roadmap-systems-engineering.md`

```
# Roadmap: Systems Engineering Hyperfixation

This roadmap focuses on turning the protocol-first scaffold into a resilient, autonomous system for managing documents, images, and mixed file types.

The current implementation is Phase 0: safe ingestion + immutable blob store + unit folders + index + audit.

## North Star

"Any file can be dropped in. The system classifies, preserves, indexes, derives useful representations, and provides multiple stable views, without losing provenance."

## System Invariants

- Originals are never deleted by automation.
- Blobs are content-addressed and immutable once stored.
- Every automated action is auditable (append-only log).
- Index is recoverable from blob store + unit manifests (best-effort).
- Low confidence or risky classifications route to quarantine.

## Operational Model

- Primary interface: CLI.
- Execution model: manual commands first; later a watcher/daemon.
- Storage model: file-first + SQLite index.

Existing Phase 0 ops helpers:
- `scripts/health.sh` (writes `.substrate/state/health.json`)
- `scripts/backup.sh` (creates tarball backups)

## Increments

### Increment 1: Safety + Quarantine (Secrets/PII)

Goal: prevent accidental propagation of sensitive materials.

Deliverables:
- secret scanning on ingest and on inbox scan
- route suspected secrets to `quarantine/` and mark unit review status
- audit events include the reason and rule id

Definition of Done:
- A file containing obvious token patterns is quarantined
- Non-secret files are not falsely quarantined in basic smoke tests
- No secret content is printed to stdout by default

### Increment 2: Derivations (OCR + Thumbnails)

Goal: make images and PDFs searchable and previewable.

Deliverables:
- derived pipeline writes to `store/derived/<sha256>/...`
- OCR text file for images (optional dependency)
- thumbnail generation for images (optional dependency)
- idempotent derivation (skip if already derived)

Definition of Done:
- Ingesting an image produces a thumbnail + OCR text when tools are present
- Derived artifacts are reproducible and tied to the blob hash

### Increment 3: Rules Engine (Routing + Unit Defaults)

Goal: turn `rules/routing.yaml` into real behavior.

Deliverables:
- rule evaluation by mime/name/content hint
- apply default `unit.type`, `tags`, and `review_status`
- store rule match results in audit + index

Definition of Done:
- A PDF auto-sets unit type to `document`
- An image auto-sets unit type to `image`
- Unmatched files remain `unknown` and `needs_review`

### Increment 4: Query UX (Search + Inspect)

Goal: make the tool usable without opening SQLite.

Deliverables:
- `autofile list-units` (most recent, with counts)
- `autofile show-unit <unit-id>` (unit.yaml + attachments)
- `autofile find-blob <sha256prefix>`
- optional: search OCR/text if derivations exist

Definition of Done:
- A user can locate the unit created for an ingested file by name/hash

### Increment 5: Daemon Mode (Watch Inbox)

Goal: autonomous operation.

Deliverables:
- polling watcher (portable) and optional inotify watcher (linux)
- lock file / single-instance protection
- crash-safe processing loop

Definition of Done:
- Dropping a file into `inbox/` results in ingestion within N seconds
- Reboots/restarts do not duplicate blobs

### Increment 6: Views + Exports

Goal: durable human browsing patterns and safe export.

Deliverables:
- views by tag, unit type, and date
- export command that copies blobs into a target directory with stable naming

Definition of Done:
- Views regenerate deterministically
- Exported sets are reproducible

### Increment 7: Reliability + Ops

Goal: make failures visible and recovery boring.

Deliverables:
- health status file under `.substrate/state/` updated on runs
- structured error events + failure counts
- DB backup routine and integrity check

Definition of Done:

(truncated: 152 lines total)
```

### `tools/autofile/autofile.py`

```
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import mimetypes
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_filename(name: str) -> str:
    # Conservative: keep alnum + a few separators.
    out = []
    for ch in name:
        if ch.isalnum() or ch in (".", "-", "_", "+"):
            out.append(ch)
        else:
            out.append("_")
    s = "".join(out).strip("._")
    return s or "file"


def _sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            h.update(chunk)
    return h.hexdigest(), size


_SECRET_PATTERNS: list[tuple[str, re.Pattern[bytes]]] = [
    ("private_key_pem", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("aws_access_key_id", re.compile(rb"AKIA[0-9A-Z]{16}")),
    ("github_token", re.compile(rb"ghp_[A-Za-z0-9]{20,}")),
    ("github_pat", re.compile(rb"github_pat_[A-Za-z0-9_]{20,}")),
    ("slack_token", re.compile(rb"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("stripe_secret", re.compile(rb"sk_(?:live|test)_[0-9A-Za-z]{10,}")),
]


def _scan_for_secrets(path: Path, ext: str | None) -> list[str]:
    # Conservative scan: look for known token formats and key material markers.
    # Avoid printing matched content.
    reasons: list[str] = []

    if ext in {"pem", "key", "p12", "pfx"}:
        reasons.append(f"sensitive_extension:{ext}")

    try:
        with path.open("rb") as f:
            data = f.read(2 * 1024 * 1024)
    except Exception:
        return reasons

    for name, pat in _SECRET_PATTERNS:
        if pat.search(data) is not None:
            reasons.append(f"pattern:{name}")

    # Additional lightweight markers.
    if b"seed phrase" in data.lower() or b"mnemonic" in data.lower():
        reasons.append("marker:seed_or_mnemonic")

    return sorted(set(reasons))


def _detect_mime(path: Path) -> str:
    # Prefer `file` if available (better than extension guess).
    try:
        cp = subprocess.run(
            ["file", "--mime-type", "-b", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        mime = cp.stdout.strip()
        if mime:
            return mime
    except Exception:
        pass

    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def _blob_path(root: Path, sha256: str) -> Path:
    shard = sha256[:2]
    return root / "store" / "blobs" / shard / sha256


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _connect_db(db_path: Path) -> sqlite3.Connection:
    _ensure_dir(db_path.parent)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _acquire_lock(root: Path) -> Path:

(truncated: 802 lines total)
```

