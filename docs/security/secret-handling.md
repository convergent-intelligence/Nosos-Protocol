# Secret Handling and Quarantine

This framework assumes any ingested content may be sensitive.

## Invariants

- Do not bake secrets into distros, ISOs, or images.
- Do not print secret contents to stdout/stderr.
- If we suspect secrets, we quarantine and require review.

## Quarantine Model

- When AutoFile detects likely secrets during ingest, it:
  - marks the unit `review_status: quarantined` (best effort)
  - writes a marker file: `quarantine/<unit-id>.json`
  - logs an audit event in `index/audit.jsonl`

## What Triggers Quarantine (Phase 1 baseline)

- known token formats (GitHub tokens, Slack tokens, etc.)
- private key markers (PEM)
- sensitive extensions (`.pem`, `.key`, `.p12`, `.pfx`)

## Review Procedure

1. Inspect the quarantine marker:
- `quarantine/<unit-id>.json`

2. Decide resolution:
- delete the blob (manual, high-risk)
- keep it but restrict access and document why
- move it to a separate encrypted store (outside scope)

3. Record the outcome:
- write an issue or decision record
- update unit `review_status` (manual edit) when resolved

## Distro/ISO Guardrail

The distro build excludes:
- blobs
- sqlite db
- audit logs
- issue/stub/capsule markdown content

See `scripts/build-distro.sh` and `distro/MANIFEST.yaml`.
