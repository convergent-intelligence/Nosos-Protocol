# Pathway: Autonomous File Organization (AutoFile)

This pathway is for teams who want a consistent, low-friction way to manage documents, images, and mixed file types autonomously.

The key idea is:
- blobs are immutable and content-addressed (hash-keyed)
- "unit folders" are human-facing manifests
- the index is machine-facing truth
- folders are views, not reality

## The Model

### Blob

A blob is a file stored by hash.

- Location: `store/blobs/<aa>/<sha256>`
- Properties: immutable, deduplicated, integrity-checked

### Unit

A unit is a coherent entity (one thing) that may have many blobs.

- Location: `units/<unit-id>/`
- Human surface:
  - `unit.yaml` stable metadata
  - `attachments.jsonl` append-only references to blobs
  - `notes.md` free-form context

### Index

The index is how the tool remains autonomous.

- `index/autofile.sqlite` relations (blobs, units, links)
- `index/audit.jsonl` append-only audit log

### Views

Views are generated representations (usually symlinks) for human convenience.

- Example: `views/by-mime/application__pdf/`

## Phase 0 Setup

From the scaffold root:

```bash
./scripts/autofile init
./scripts/validate.sh
```

## Day-to-Day Workflow

### 1) Drop files into the inbox

Put any file into `inbox/`.

### 2) Scan the inbox

```bash
./scripts/autofile scan-inbox
```

Or run continuously:

```bash
./scripts/autofile watch-inbox --interval 2
```

Results:
- ingested files move to `inbox/processed/`
- failures move to `inbox/failed/`

### 3) Build views

```bash
./scripts/autofile build-views
```

### 3.5) Generate derived artifacts (optional)

If ImageMagick and/or pdftotext are present, you can generate:
- thumbnails for images
- extracted text for PDFs

```bash
./scripts/autofile derive --all
```

### 4) Inspect unit folders

Each ingested file creates (by default) a new unit folder under `units/`.

Unit defaults (type) are applied via `rules/routing.yaml`.

If you want multiple files in one unit:

```bash
./scripts/autofile ingest path/to/dir --unit U-20260130-000000-acde12
```

### 5) Query without opening SQLite

```bash
./scripts/autofile list-units
./scripts/autofile show-unit U-...
./scripts/autofile find-blob abcd12
```

## Safety Properties

- Originals are not deleted by the ingest command.
- Blobs are content-addressed and deduplicated.
- Audit log is append-only (`index/audit.jsonl`).
- Unit attachment logs are append-only (`attachments.jsonl`).

## What To Extend Next (Phase 1+)

- Secret scanning (route to `quarantine/`)
- OCR for images and PDFs (write to `store/derived/<hash>/`)
- Routing rules (use `rules/routing.yaml` to set default unit type/tags)
- Better mime detection / file signatures
- Additional views (by tag, by date, by unit type)
