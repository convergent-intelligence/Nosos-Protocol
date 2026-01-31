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

        # End `when:` block when we hit another top-level route field.
        if line.startswith("default_unit_type:"):
            in_when = False
            _, v = line.split(":", 1)
            if cur is not None:
                cur["default_unit_type"] = v.strip().strip('"').strip("'")
            continue

        if line.startswith("-") and "name:" in line:
            if cur is not None:
                routes.append(cur)
            cur = {"when": {}}
            in_when = False
            _, v = line.split("name:", 1)
            cur["name"] = v.strip().strip('"').strip("'")
            continue

        if cur is None:
            continue

        if line == "when:":
            in_when = True
            continue

        if in_when:
            if ":" in line:
                k, v = line.split(":", 1)
                cur["when"][k.strip()] = v.strip().strip('"').strip("'")
            continue

    if cur is not None:
        routes.append(cur)
    return routes


def _select_route(routes: list[dict], mime: str) -> dict | None:
    for r in routes:
        when = r.get("when") or {}
        mime_prefix = when.get("mime_prefix")
        if mime_prefix and mime.startswith(str(mime_prefix)):
            return r
        mime_is = when.get("mime_is")
        if mime_is and mime == str(mime_is):
            return r
        any_ = when.get("any")
        if str(any_).lower() == "true":
            return r
    return None


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
    """Single-instance lock.

    Uses an atomic create to avoid platform-specific locking calls.
    """

    lock_path = root / "index" / "autofile.lock"
    _ensure_dir(lock_path.parent)
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise RuntimeError(f"lock exists: {lock_path}")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(f"pid={os.getpid()}\n")
        f.write(f"ts={_utc_now_rfc3339()}\n")
    return lock_path


def _release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def _init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS blobs (
          sha256 TEXT PRIMARY KEY,
          size_bytes INTEGER NOT NULL,
          mime TEXT NOT NULL,
          ext TEXT,
          first_seen_at TEXT NOT NULL,
          original_name TEXT
        );

        CREATE TABLE IF NOT EXISTS units (
          unit_id TEXT PRIMARY KEY,
          created_at TEXT NOT NULL,
          title TEXT,
          type TEXT,
          review_status TEXT
        );

        CREATE TABLE IF NOT EXISTS unit_attachments (
          unit_id TEXT NOT NULL,
          sha256 TEXT NOT NULL,
          role TEXT NOT NULL,
          attached_at TEXT NOT NULL,
          UNIQUE(unit_id, sha256, role),
          FOREIGN KEY(unit_id) REFERENCES units(unit_id) ON DELETE CASCADE,
          FOREIGN KEY(sha256) REFERENCES blobs(sha256) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          ts TEXT NOT NULL,
          action TEXT NOT NULL,
          payload_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS derived (
          sha256 TEXT NOT NULL,
          kind TEXT NOT NULL,
          path TEXT NOT NULL,
          created_at TEXT NOT NULL,
          UNIQUE(sha256, kind),
          FOREIGN KEY(sha256) REFERENCES blobs(sha256) ON DELETE CASCADE
        );
        """
    )
    conn.commit()


def _append_audit(root: Path, action: str, payload: dict) -> None:
    entry = {
        "ts": _utc_now_rfc3339(),
        "action": action,
        "payload": payload,
    }
    audit_path = root / "index" / "audit.jsonl"
    _ensure_dir(audit_path.parent)
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def _db_event(conn: sqlite3.Connection, action: str, payload: dict) -> None:
    conn.execute(
        "INSERT INTO events(ts, action, payload_json) VALUES (?, ?, ?)",
        (_utc_now_rfc3339(), action, json.dumps(payload, sort_keys=True)),
    )
    conn.commit()


def _unit_dir(root: Path, unit_id: str) -> Path:
    return root / "units" / unit_id


def _write_unit_yaml_if_missing(unit_dir: Path, unit_id: str) -> None:
    path = unit_dir / "unit.yaml"
    if not path.exists():
        content = (
            "version: 0.1\n"
            f"unit_id: {unit_id}\n"
            f"created_at: {_utc_now_rfc3339()}\n"
            "title: \"\"\n"
            "type: \"unknown\"\n"
            "review_status: needs_review\n"
            "tags: []\n"
            "links: []\n"
        )
        path.write_text(content, encoding="utf-8")

    notes = unit_dir / "notes.md"
    if not notes.exists():
        notes.write_text("# Notes\n\n", encoding="utf-8")

    attachments = unit_dir / "attachments.jsonl"
    if not attachments.exists():
        attachments.write_text("", encoding="utf-8")

    derived = unit_dir / "derived.jsonl"
    if not derived.exists():
        derived.write_text("", encoding="utf-8")


def _set_unit_yaml_field(
    unit_dir: Path,
    key: str,
    value: str,
    *,
    only_if_values: set[str] | None = None,
) -> bool:
    """Best-effort YAML line edit without a YAML parser.

    - Updates the first `key:` line.
    - If `only_if_values` is provided, only updates when current value matches.
    - Returns True when a change is made.
    """

    p = unit_dir / "unit.yaml"
    if not p.exists():
        return False

    lines = p.read_text(encoding="utf-8").splitlines(True)
    changed = False
    found = False
    prefix = f"{key}:"
    for i, line in enumerate(lines):
        if not line.startswith(prefix):
            continue
        found = True
        current = line[len(prefix) :].strip()
        if only_if_values is not None and current not in only_if_values:
            return False
        lines[i] = f"{key}: {value}\n"
        changed = True
        break

    if not found:
        lines.append(f"{key}: {value}\n")
        changed = True

    if changed:
        p.write_text("".join(lines), encoding="utf-8")
    return changed


def _write_quarantine_marker(root: Path, unit_id: str, payload: dict) -> Path:
    qdir = root / "quarantine"
    _ensure_dir(qdir)
    path = qdir / f"{unit_id}.json"
    if not path.exists():
        path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path


def _append_unit_attachment_event(unit_dir: Path, event: dict) -> None:
    path = unit_dir / "attachments.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")


def _append_unit_derived_event(unit_dir: Path, event: dict) -> None:
    path = unit_dir / "derived.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")


def _create_unit_id(sha256: str) -> str:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"U-{ts}-{sha256[:6]}"


@dataclass(frozen=True)
class IngestResult:
    sha256: str
    stored_at: Path
    unit_id: str
    mime: str
    size_bytes: int
    quarantined: bool


def ingest_file(root: Path, conn: sqlite3.Connection, path: Path, unit_id: str | None) -> IngestResult:
    if not path.exists() or not path.is_file():
        raise ValueError(f"not a file: {path}")

    sha256, size_bytes = _sha256_file(path)
    mime = _detect_mime(path)
    ext = path.suffix.lower().lstrip(".") if path.suffix else None

    secret_reasons = _scan_for_secrets(path, ext)

    blob_path = _blob_path(root, sha256)
    _ensure_dir(blob_path.parent)
    if not blob_path.exists():
        tmp = blob_path.with_suffix(".tmp")
        shutil.copy2(path, tmp)
        os.replace(tmp, blob_path)

    conn.execute(
        "INSERT OR IGNORE INTO blobs(sha256, size_bytes, mime, ext, first_seen_at, original_name) VALUES (?, ?, ?, ?, ?, ?)",
        (sha256, size_bytes, mime, ext, _utc_now_rfc3339(), path.name),
    )
    conn.commit()

    if unit_id is None:
        unit_id = _create_unit_id(sha256)

    unit_dir = _unit_dir(root, unit_id)
    _ensure_dir(unit_dir)
    _write_unit_yaml_if_missing(unit_dir, unit_id)

    conn.execute(
        "INSERT OR IGNORE INTO units(unit_id, created_at, title, type, review_status) VALUES (?, ?, ?, ?, ?)",
        (unit_id, _utc_now_rfc3339(), "", "unknown", "needs_review"),
    )
    conn.commit()

    # Apply routing defaults (rules/routing.yaml).
    routes = _load_routes(root)
    route = _select_route(routes, mime)
    if route is not None:
        default_type = route.get("default_unit_type")
        if default_type and _set_unit_yaml_field(unit_dir, "type", f'"{default_type}"', only_if_values={'"unknown"'}):
            conn.execute(
                "UPDATE units SET type=? WHERE unit_id=? AND (type IS NULL OR type='' OR type='unknown')",
                (str(default_type), unit_id),
            )
            conn.commit()
        _append_audit(
            root,
            "route_match",
            {"unit_id": unit_id, "sha256": sha256, "mime": mime, "route": route.get("name", "")},
        )
        _db_event(
            conn,
            "route_match",
            {"unit_id": unit_id, "sha256": sha256, "mime": mime, "route": route.get("name", "")},
        )

    conn.execute(
        "INSERT OR IGNORE INTO unit_attachments(unit_id, sha256, role, attached_at) VALUES (?, ?, ?, ?)",
        (unit_id, sha256, "original", _utc_now_rfc3339()),
    )
    conn.commit()

    quarantined = False
    quarantine_path: str | None = None
    if secret_reasons:
        quarantined = True
        # Mark unit as quarantined (best effort; do not overwrite explicit user edits).
        _set_unit_yaml_field(unit_dir, "review_status", "quarantined", only_if_values={"needs_review", ""})
        conn.execute(
            "UPDATE units SET review_status=? WHERE unit_id=? AND (review_status IS NULL OR review_status='' OR review_status='needs_review')",
            ("quarantined", unit_id),
        )
        conn.commit()

        qpayload = {
            "ts": _utc_now_rfc3339(),
            "unit_id": unit_id,
            "sha256": sha256,
            "source_path": str(path),
            "reasons": secret_reasons,
        }
        quarantine_path = str(_write_quarantine_marker(root, unit_id, qpayload))
        _append_audit(root, "quarantine", {"unit_id": unit_id, "sha256": sha256, "reasons": secret_reasons, "marker": quarantine_path})
        _db_event(conn, "quarantine", {"unit_id": unit_id, "sha256": sha256, "reasons": secret_reasons, "marker": quarantine_path})

    unit_event = {
        "ts": _utc_now_rfc3339(),
        "unit_id": unit_id,
        "sha256": sha256,
        "role": "original",
        "source_path": str(path),
        "mime": mime,
        "size_bytes": size_bytes,
    }
    _append_unit_attachment_event(unit_dir, unit_event)

    payload = {
        "sha256": sha256,
        "mime": mime,
        "size_bytes": size_bytes,
        "unit_id": unit_id,
        "source_path": str(path),
        "blob_path": str(blob_path),
        "quarantined": quarantined,
        "quarantine_marker": quarantine_path,
    }
    _append_audit(root, "ingest", payload)
    _db_event(conn, "ingest", payload)

    return IngestResult(
        sha256=sha256,
        stored_at=blob_path,
        unit_id=unit_id,
        mime=mime,
        size_bytes=size_bytes,
        quarantined=quarantined,
    )


def ingest_path(root: Path, conn: sqlite3.Connection, p: Path, unit_id: str | None) -> list[IngestResult]:
    results: list[IngestResult] = []
    if p.is_file():
        results.append(ingest_file(root, conn, p, unit_id))
        return results
    if not p.is_dir():
        raise ValueError(f"not a file or directory: {p}")

    for child in sorted(p.rglob("*")):
        if not child.is_file():
            continue
        results.append(ingest_file(root, conn, child, unit_id))
    return results


def build_views(root: Path, conn: sqlite3.Connection) -> int:
    cur = conn.execute("SELECT sha256, mime, ext, original_name FROM blobs")
    rows = cur.fetchall()
    count = 0
    for sha256, mime, ext, original_name in rows:
        mime_dir = mime.replace("/", "__")
        view_dir = root / "views" / "by-mime" / mime_dir
        _ensure_dir(view_dir)

        name_hint = _safe_filename(original_name or sha256)
        suffix = f".{ext}" if ext and not name_hint.endswith(f".{ext}") else ""
        link_name = f"{sha256[:12]}_{name_hint}{suffix}"
        link_path = view_dir / link_name

        target = _blob_path(root, sha256)
        if link_path.exists():
            continue
        try:
            os.symlink(target, link_path)
        except Exception:
            # Fall back to a copy if symlinks are not supported.
            shutil.copy2(target, link_path)
        count += 1

    payload = {"created": count}
    _append_audit(root, "build_views", payload)
    _db_event(conn, "build_views", payload)
    return count


def _which(cmd: str) -> str | None:
    return shutil.which(cmd)


def _derive_thumbnail(root: Path, sha256: str, *, force: bool) -> str | None:
    in_path = _blob_path(root, sha256)
    out_dir = root / "store" / "derived" / sha256
    _ensure_dir(out_dir)
    out_path = out_dir / "thumb.jpg"
    if out_path.exists() and not force:
        return str(out_path)

    tool = _which("magick") or _which("convert")
    if tool is None:
        return None

    cmd = [tool, str(in_path), "-auto-orient", "-strip", "-thumbnail", "512x512>", str(out_path)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return str(out_path)


def _derive_pdf_text(root: Path, sha256: str, *, force: bool) -> str | None:
    in_path = _blob_path(root, sha256)
    out_dir = root / "store" / "derived" / sha256
    _ensure_dir(out_dir)
    out_path = out_dir / "text.txt"
    if out_path.exists() and not force:
        return str(out_path)

    tool = _which("pdftotext")
    if tool is None:
        return None

    cmd = [tool, "-layout", str(in_path), str(out_path)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return str(out_path)


def derive_blob(root: Path, conn: sqlite3.Connection, sha256: str, *, force: bool) -> dict:
    row = conn.execute("SELECT mime FROM blobs WHERE sha256=?", (sha256,)).fetchone()
    if row is None:
        raise ValueError(f"unknown blob: {sha256}")
    mime = row[0]

    results: list[dict] = []
    errors: list[dict] = []

    def record(kind: str, path: str) -> None:
        conn.execute(
            "INSERT OR REPLACE INTO derived(sha256, kind, path, created_at) VALUES (?, ?, ?, ?)",
            (sha256, kind, path, _utc_now_rfc3339()),
        )
        conn.commit()
        results.append({"kind": kind, "path": path})

        cur = conn.execute("SELECT unit_id FROM unit_attachments WHERE sha256=?", (sha256,))
        for (unit_id,) in cur.fetchall():
            unit_dir = _unit_dir(root, unit_id)
            if unit_dir.exists():
                _append_unit_derived_event(
                    unit_dir,
                    {
                        "ts": _utc_now_rfc3339(),
                        "unit_id": unit_id,
                        "sha256": sha256,
                        "kind": kind,
                        "path": path,
                    },
                )

    try:
        if mime.startswith("image/"):
            p = _derive_thumbnail(root, sha256, force=force)
            if p is not None:
                record("thumbnail", p)
        elif mime == "application/pdf":
            p = _derive_pdf_text(root, sha256, force=force)
            if p is not None:
                record("text", p)
    except subprocess.CalledProcessError as e:
        errors.append({"error": "subprocess_failed", "detail": str(e)})
    except Exception as e:
        errors.append({"error": "derive_failed", "detail": str(e)})

    payload = {"sha256": sha256, "mime": mime, "results": results, "errors": errors}
    _append_audit(root, "derive", payload)
    _db_event(conn, "derive", payload)
    return payload


def scan_inbox(root: Path, conn: sqlite3.Connection) -> tuple[int, int]:
    inbox = root / "inbox"
    processed = inbox / "processed"
    failed = inbox / "failed"
    _ensure_dir(processed)
    _ensure_dir(failed)

    ok = 0
    bad = 0
    for p in sorted(inbox.iterdir()):
        if p.name in ("processed", "failed"):
            continue
        if not p.is_file():
            continue
        try:
            ingest_file(root, conn, p, unit_id=None)
            stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
            dest = processed / f"{stamp}_{_safe_filename(p.name)}"
            os.replace(p, dest)
            ok += 1
        except Exception as e:
            stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
            dest = failed / f"{stamp}_{_safe_filename(p.name)}"
            try:
                os.replace(p, dest)
            except Exception:
                pass
            payload = {"path": str(p), "error": str(e)}
            _append_audit(root, "scan_inbox_failed", payload)
            _db_event(conn, "scan_inbox_failed", payload)
            bad += 1

    payload = {"ok": ok, "failed": bad}
    _append_audit(root, "scan_inbox", payload)
    _db_event(conn, "scan_inbox", payload)
    return ok, bad


def status(root: Path, conn: sqlite3.Connection) -> dict:
    blobs = conn.execute("SELECT COUNT(*) FROM blobs").fetchone()[0]
    units = conn.execute("SELECT COUNT(*) FROM units").fetchone()[0]
    attachments = conn.execute("SELECT COUNT(*) FROM unit_attachments").fetchone()[0]
    quarantined = conn.execute("SELECT COUNT(*) FROM units WHERE review_status='quarantined'").fetchone()[0]
    return {
        "root": str(root),
        "blobs": blobs,
        "units": units,
        "attachments": attachments,
        "quarantined_units": quarantined,
        "db": str(root / "index" / "autofile.sqlite"),
    }


def list_units(conn: sqlite3.Connection, limit: int) -> list[dict]:
    cur = conn.execute(
        """
        SELECT u.unit_id, u.created_at, u.type, u.review_status, COUNT(a.sha256) AS attachment_count
        FROM units u
        LEFT JOIN unit_attachments a ON a.unit_id = u.unit_id
        GROUP BY u.unit_id
        ORDER BY u.created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    out: list[dict] = []
    for unit_id, created_at, utype, review_status, attachment_count in cur.fetchall():
        out.append(
            {
                "unit_id": unit_id,
                "created_at": created_at,
                "type": utype,
                "review_status": review_status,
                "attachment_count": attachment_count,
                "unit_dir": str(_unit_dir(_resolve_root(), unit_id)),
            }
        )
    return out


def show_unit(root: Path, conn: sqlite3.Connection, unit_id: str) -> dict:
    u = conn.execute(
        "SELECT unit_id, created_at, title, type, review_status FROM units WHERE unit_id=?",
        (unit_id,),
    ).fetchone()
    if u is None:
        raise ValueError(f"unknown unit: {unit_id}")

    unit_dir = _unit_dir(root, unit_id)
    unit_yaml = None
    unit_yaml_path = unit_dir / "unit.yaml"
    if unit_yaml_path.exists():
        unit_yaml = unit_yaml_path.read_text(encoding="utf-8")

    attachments: list[dict] = []
    cur = conn.execute(
        """
        SELECT a.sha256, a.role, a.attached_at, b.mime, b.size_bytes
        FROM unit_attachments a
        JOIN blobs b ON b.sha256 = a.sha256
        WHERE a.unit_id=?
        ORDER BY a.attached_at ASC
        """,
        (unit_id,),
    )
    for sha256, role, attached_at, mime, size_bytes in cur.fetchall():
        attachments.append(
            {
                "sha256": sha256,
                "role": role,
                "attached_at": attached_at,
                "mime": mime,
                "size_bytes": size_bytes,
                "blob_path": str(_blob_path(root, sha256)),
            }
        )

    return {
        "unit": {
            "unit_id": u[0],
            "created_at": u[1],
            "title": u[2],
            "type": u[3],
            "review_status": u[4],
        },
        "unit_dir": str(unit_dir),
        "unit_yaml": unit_yaml,
        "attachments": attachments,
    }


def find_blob(conn: sqlite3.Connection, prefix: str, limit: int) -> list[dict]:
    prefix = prefix.strip().lower()
    if not prefix:
        raise ValueError("prefix is required")
    cur = conn.execute(
        "SELECT sha256, mime, size_bytes, original_name, first_seen_at FROM blobs WHERE sha256 LIKE ? LIMIT ?",
        (prefix + "%", limit),
    )
    out: list[dict] = []
    for sha256, mime, size_bytes, original_name, first_seen_at in cur.fetchall():
        out.append(
            {
                "sha256": sha256,
                "mime": mime,
                "size_bytes": size_bytes,
                "original_name": original_name,
                "first_seen_at": first_seen_at,
            }
        )
    return out


def _resolve_root() -> Path:
    env = os.environ.get("AUTOFILE_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    # tools/autofile/autofile.py -> root is ../..
    return Path(__file__).resolve().parents[2]


def cmd_init(args: argparse.Namespace) -> int:
    root = _resolve_root()
    for p in (
        root / "inbox",
        root / "inbox" / "processed",
        root / "inbox" / "failed",
        root / "store" / "blobs",
        root / "store" / "derived",
        root / "index",
        root / "views",
        root / "rules",
        root / "units",
        root / "quarantine",
    ):
        _ensure_dir(p)

    db_path = root / "index" / "autofile.sqlite"
    conn = _connect_db(db_path)
    _init_db(conn)
    _append_audit(root, "init", {"db": str(db_path)})
    _db_event(conn, "init", {"db": str(db_path)})
    print(json.dumps({"ok": True, "root": str(root), "db": str(db_path)}, indent=2))
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)

    p = Path(args.path).expanduser().resolve()
    results = ingest_path(root, conn, p, unit_id=args.unit)
    out = []
    for r in results:
        out.append(
            {
                "sha256": r.sha256,
                "stored_at": str(r.stored_at),
                "unit_id": r.unit_id,
                "mime": r.mime,
                "size_bytes": r.size_bytes,
                "quarantined": r.quarantined,
            }
        )
    print(json.dumps(out, indent=2))
    return 0


def cmd_scan_inbox(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)
    ok, bad = scan_inbox(root, conn)
    print(json.dumps({"ok": ok, "failed": bad}, indent=2))
    return 0


def cmd_build_views(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)
    created = build_views(root, conn)
    print(json.dumps({"created": created}, indent=2))
    return 0


def cmd_derive(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)

    force = bool(args.force)
    out: list[dict] = []

    if args.all:
        cur = conn.execute("SELECT sha256 FROM blobs")
        for (sha256,) in cur.fetchall():
            out.append(derive_blob(root, conn, sha256, force=force))
    elif args.unit:
        cur = conn.execute("SELECT sha256 FROM unit_attachments WHERE unit_id=?", (args.unit,))
        for (sha256,) in cur.fetchall():
            out.append(derive_blob(root, conn, sha256, force=force))
    elif args.sha:
        out.append(derive_blob(root, conn, args.sha, force=force))
    else:
        raise SystemExit("provide --sha, --unit, or --all")

    print(json.dumps(out, indent=2))
    return 0


def cmd_watch_inbox(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)

    interval = float(args.interval)
    if interval < 0.25:
        interval = 0.25

    lock_path = _acquire_lock(root)
    try:
        _append_audit(root, "watch_start", {"interval": interval, "build_views": bool(args.build_views)})
        _db_event(conn, "watch_start", {"interval": interval, "build_views": bool(args.build_views)})

        while True:
            ok, bad = scan_inbox(root, conn)
            created = 0
            if args.build_views:
                created = build_views(root, conn)

            if args.json:
                print(json.dumps({"ok": ok, "failed": bad, "views_created": created, "ts": _utc_now_rfc3339()}, indent=2))
            else:
                print(f"{_utc_now_rfc3339()} ok={ok} failed={bad} views_created={created}")

            if args.once:
                break
            time.sleep(interval)

        _append_audit(root, "watch_stop", {})
        _db_event(conn, "watch_stop", {})
        return 0
    finally:
        _release_lock(lock_path)


def cmd_status(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)
    print(json.dumps(status(root, conn), indent=2))
    return 0


def cmd_list_units(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)
    print(json.dumps(list_units(conn, limit=int(args.limit)), indent=2))
    return 0


def cmd_show_unit(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)
    print(json.dumps(show_unit(root, conn, args.unit_id), indent=2))
    return 0


def cmd_find_blob(args: argparse.Namespace) -> int:
    root = _resolve_root()
    conn = _connect_db(root / "index" / "autofile.sqlite")
    _init_db(conn)
    print(json.dumps(find_blob(conn, args.prefix, limit=int(args.limit)), indent=2))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="autofile")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="initialize directories and database")
    p_init.set_defaults(fn=cmd_init)

    p_ingest = sub.add_parser("ingest", help="ingest a file or directory")
    p_ingest.add_argument("path")
    p_ingest.add_argument("--unit", help="attach to an existing unit id")
    p_ingest.set_defaults(fn=cmd_ingest)

    p_scan = sub.add_parser("scan-inbox", help="ingest all files in inbox/")
    p_scan.set_defaults(fn=cmd_scan_inbox)

    p_views = sub.add_parser("build-views", help="(re)build generated views")
    p_views.set_defaults(fn=cmd_build_views)

    p_derive = sub.add_parser("derive", help="generate derived artifacts (thumbnails/text)")
    p_derive.add_argument("--sha")
    p_derive.add_argument("--unit")
    p_derive.add_argument("--all", action="store_true")
    p_derive.add_argument("--force", action="store_true")
    p_derive.set_defaults(fn=cmd_derive)

    p_watch = sub.add_parser("watch-inbox", help="watch inbox/ and ingest continuously")
    p_watch.add_argument("--interval", default="2.0", help="poll interval seconds")
    p_watch.add_argument("--once", action="store_true", help="run a single iteration")
    p_watch.add_argument("--no-build-views", dest="build_views", action="store_false")
    p_watch.add_argument("--json", action="store_true", help="emit JSON per iteration")
    p_watch.set_defaults(fn=cmd_watch_inbox, build_views=True)

    p_status = sub.add_parser("status", help="print index counts")
    p_status.set_defaults(fn=cmd_status)

    p_list = sub.add_parser("list-units", help="list recent units")
    p_list.add_argument("--limit", default="20")
    p_list.set_defaults(fn=cmd_list_units)

    p_show = sub.add_parser("show-unit", help="show a unit and its attachments")
    p_show.add_argument("unit_id")
    p_show.set_defaults(fn=cmd_show_unit)

    p_find = sub.add_parser("find-blob", help="find blobs by sha256 prefix")
    p_find.add_argument("prefix")
    p_find.add_argument("--limit", default="25")
    p_find.set_defaults(fn=cmd_find_blob)

    args = parser.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
