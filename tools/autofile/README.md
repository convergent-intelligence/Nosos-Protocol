# AutoFile

AutoFile is a tiny, file-first ingestion tool.

It takes arbitrary files (docs, images, anything), fingerprints them, stores them in a content-addressed blob store, and records how they relate to "units" (work packets / entities).

Design goals:
- safe by default (never deletes originals)
- deterministic storage (hash-addressed)
- append-only human surfaces (unit folders) + indexed truth (SQLite)
- minimal dependencies (Python stdlib; optional `file` command)

## Layout

- `inbox/` drop zone (tool processes files from here)
- `store/blobs/` immutable content-addressed storage
- `index/autofile.sqlite` index database (blobs, units, attachments)
- `index/audit.jsonl` append-only audit log
- `units/<unit-id>/` unit folders (human-facing)
- `views/` generated views (symlinks) by mime/type

## Usage

Run from the scaffold root:

```bash
./scripts/autofile init
./scripts/autofile ingest path/to/file.pdf
./scripts/autofile scan-inbox
./scripts/autofile watch-inbox
./scripts/autofile derive --all
./scripts/autofile build-views
./scripts/autofile status
./scripts/autofile list-units
./scripts/autofile show-unit U-...
./scripts/autofile find-blob deadbeef
```

If you want to attach to an existing unit:

```bash
./scripts/autofile ingest path/to/photo.jpg --unit U-20260130-000000-acde12
```

## What Gets Written

- Blob stored at `store/blobs/<aa>/<sha256>`
- Unit folder created at `units/<unit-id>/`
  - `unit.yaml` (stable metadata)
  - `attachments.jsonl` (append-only attachment events)
  - `notes.md` (optional free-form)
- Index updated in `index/autofile.sqlite`
- Audit event appended to `index/audit.jsonl`

If AutoFile suspects secrets, it will:
- mark the unit `review_status: quarantined` (best effort)
- write a marker file: `quarantine/<unit-id>.json`

## Extending

Routing/classification rules live in `rules/routing.yaml`.
Phase 0 keeps this intentionally minimal.

Current behavior:
- AutoFile reads `rules/routing.yaml` on ingest and applies `default_unit_type` to new units.

For the next planned increments (secrets/quarantine, OCR/thumbnails, rules engine, daemon mode), see:
- `docs/roadmap-systems-engineering.md`
