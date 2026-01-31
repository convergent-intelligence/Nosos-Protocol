# System Brief (Draft)

## One Sentence

Agent Systems Framework: a protocol-first scaffold and toolchain for orchestrating systems work (plans/issues/stubs) and autonomous file ingestion (docs/images) with auditability.

## Users

- Operators and builders shipping a repeatable systems workflow
- Agents (Watcher/Builder/Guardian/Scribe/Gems) collaborating via files and signals

## Non-Goals

- A full ticketing system replacement (it is file-first, intentionally small)
- A secret manager (it detects and quarantines likely secrets, but does not store/rotate them)
- A production deployment platform (deployment is planned and documented, not assumed)

## Interfaces

- Input: files dropped into `inbox/`, edits to YAML/MD planning surfaces, CLI commands
- Output: content-addressed blob storage, unit folders, audit/index files, generated views, signal files

## Data

- Data types: blobs (immutable), unit manifests, audit/events, plans/issues/stubs, signals
- Sensitive data: any ingested content may be sensitive; treat `store/blobs/` and `index/` as sensitive by default
- Source of truth: `store/blobs/` + `index/autofile.sqlite` for ingestion; `tools/plan-registry/plans.yaml` for work state

## Dependencies

- External: Python 3, `tar`, optional `file(1)`
- Internal: AutoFile, Orchestrator, Signals, Work, Context

## Risks

- Security: accidental ingestion of secrets (mitigated by quarantine + no-secret printing)
- Reliability: index corruption or partial state (mitigated by backups + audit + rebuild pathways)
- Cost: blob store growth (mitigated by dedupe + excluding blobs from distros by default)

## Success

- Healthy: `./scripts/validate.sh` passes; `./scripts/health.sh` produces green/yellow/red with clear next actions
- Done: a distro can be built/verified; work items can be assigned with bounded context; ingestion is autonomous and auditable
