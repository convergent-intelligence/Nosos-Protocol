# Context Capsule: Rules engine: apply routing.yaml to unit defaults

Work ID: P1-003
Kind: plan
Domain: scribe
Priority: medium
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:49:40Z

## Objective

Partial: minimal type defaults for image/pdf done; remaining: evaluate rules/routing.yaml (tags, review_status, audit rule ids)

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
- `rules/routing.yaml`
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
- `.bridges/signals/20260130-044643_proclamation_plan.json`
- `.bridges/signals/20260130-044642_missive_assignment.json`
- `.bridges/signals/20260130-044642_proclamation_plan.json`
- `.bridges/signals/20260130-044618_proclamation_plan.json`
- `.bridges/signals/20260130-044618_missive_assignment.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `rules/routing.yaml`

```
version: 0.1

# Phase 0 routing rules are intentionally minimal.
# The index (SQLite) is the source of truth; rules are hints.

routes:
  - name: "images"
    when:
      mime_prefix: "image/"
    default_unit_type: "image"

  - name: "pdf"
    when:
      mime_is: "application/pdf"
    default_unit_type: "document"

  - name: "fallback"
    when:
      any: true
    default_unit_type: "unknown"
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


def _load_routes(root: Path) -> list[dict]:
    """Load routing rules from rules/routing.yaml.

    Minimal parser for the very small subset we use.
    """

    path = root / "rules" / "routing.yaml"
    if not path.exists():
        return []

    routes: list[dict] = []
    cur: dict | None = None
    in_when = False

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

(truncated: 1023 lines total)
```

