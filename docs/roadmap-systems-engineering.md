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
- A single command produces a health snapshot and highlights failures

### Increment 8: Monitoring Surfaces (Watcher)

Goal: define and maintain the health model of the system.

Deliverables:
- explicit health signals (green/yellow/red) and what triggers them
- a minimal dashboard spec (even if implemented as CLI output)
- incident template and anomaly capture procedure

Definition of Done:
- health state can be computed from index + last run results
- anomalies are recorded consistently

### Increment 9: Administration Surfaces (Builder)

Goal: make operations boring.

Deliverables:
- backup and restore procedure for blobs + sqlite + audit
- integrity checks (blob presence, db foreign keys, audit continuity)
- safe upgrade procedure for schema changes

Definition of Done:
- a restore-from-backup drill succeeds on a fresh directory

## Interfaces to Stabilize Early

- `unit.yaml` schema (fields, defaults)
- audit event schema (`index/audit.jsonl`)
- blob path convention (`store/blobs/<aa>/<sha256>`)
