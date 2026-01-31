# Context Capsule: Fill system brief

Work ID: P0-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T03:55:36Z

## Objective

Define purpose, users, boundaries, and success criteria

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
- `docs/system-brief.md`
- `artifacts/contexts/P0-001_fill-system-brief.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=1 units=2 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-035536_missive_assignment.json`
- `.bridges/signals/20260130-035536_proclamation_plan.json`
- `.bridges/signals/20260130-035509_missive_assignment.json`
- `.bridges/signals/20260130-034638_council_call_deploy.json`
- `.bridges/signals/20260130-034431_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/system-brief.md`

```
# System Brief (Draft)

## One Sentence

<What is this system, in one sentence?>

## Users

- <primary user>
- <secondary user>

## Non-Goals

- <what this is explicitly not>

## Interfaces

- Input: <API/CLI/files/events>
- Output: <API/CLI/files/events>

## Data

- What data exists?
- What data is sensitive?
- Where is the source of truth?

## Dependencies

- External systems:
- Internal modules:

## Risks

- Security:
- Reliability:
- Cost:

## Success

- What does “healthy” look like?
- What does “done” look like?
```

### `artifacts/contexts/P0-001_fill-system-brief.md`

```
# Context Capsule: Fill system brief

Work ID: P0-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T03:55:36Z

## Objective

Define purpose, users, boundaries, and success criteria

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
- `docs/system-brief.md`
- `artifacts/contexts/P0-001_fill-system-brief.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=1 units=2 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-035536_proclamation_plan.json`
- `.bridges/signals/20260130-035509_missive_assignment.json`
- `.bridges/signals/20260130-034638_council_call_deploy.json`
- `.bridges/signals/20260130-034431_proclamation_plan.json`
- `.bridges/signals/20260130-034426_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/system-brief.md`

```
# System Brief (Draft)

## One Sentence

<What is this system, in one sentence?>

## Users

- <primary user>
- <secondary user>

## Non-Goals

- <what this is explicitly not>

## Interfaces

- Input: <API/CLI/files/events>
- Output: <API/CLI/files/events>

## Data

- What data exists?
- What data is sensitive?
- Where is the source of truth?

## Dependencies

- External systems:
- Internal modules:

## Risks

- Security:
- Reliability:
- Cost:

## Success

- What does “healthy” look like?
- What does “done” look like?
```

### `artifacts/contexts/P0-001_fill-system-brief.md`

```
# Context Capsule: Fill system brief

Work ID: P0-001
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T03:55:09Z

## Objective

(truncated: 215 lines total)
```

