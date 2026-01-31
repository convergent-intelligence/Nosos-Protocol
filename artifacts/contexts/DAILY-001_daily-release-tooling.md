# Context Capsule: Daily release tooling

Work ID: DAILY-001
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:49:27Z

## Objective

One post per day: create draft from blogwatch sources and publish into posts index

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
- `docs/publish/daily-release.md`
- `scripts/daily`
- `scripts/publish`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-054416_proclamation_plan.json`
- `.bridges/signals/20260130-053604_proclamation_plan.json`
- `.bridges/signals/20260130-053305_proclamation_plan.json`
- `.bridges/signals/20260130-052924_proclamation_plan.json`
- `.bridges/signals/20260130-052559_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/publish/daily-release.md`

```
# Daily Release: 1 Post Per Day

Goal: one evidence-first post per day in a chosen knowledge domain.

Principles:
- we do not publish vibes
- every post links to artifacts and commands that reproduce the claim

## Create Today’s Draft

Pick a domain from BlogWatch:

```bash
./scripts/blogwatch domains
```

Create the draft (and fetch sources):

```bash
./scripts/daily --domain mathematics
```

Draft path:
- `sites/convergent-intelligence/drafts/YYYY-MM-DD_<domain>.md`

## Publish (Local)

Publishing moves the draft into date-based posts and updates an index:

```bash
./scripts/publish sites/convergent-intelligence/drafts/YYYY-MM-DD_mathematics.md
```

## Evidence

Source ingestion artifacts live under:
- `artifacts/blogwatch/<domain>/`

Daily creation record lives under:
- `artifacts/publish/daily/`
```

### `scripts/daily`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/publish/daily.py" "$@"
```

### `scripts/publish`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/publish/publish.py" "$@"
```

