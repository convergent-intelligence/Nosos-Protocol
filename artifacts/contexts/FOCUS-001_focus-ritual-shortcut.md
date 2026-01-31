# Context Capsule: Focus ritual shortcut

Work ID: FOCUS-001
Kind: plan
Domain: scribe
Priority: medium
Status: in_progress
Owner: scribe
Generated: 2026-01-30T05:13:35Z

## Objective

One-command shortcut that writes .substrate/state/focus.json (health+field+budgets+queue)

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
- `scripts/focus`
- `docs/ops/focus.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-051043_proclamation_plan.json`
- `.bridges/signals/20260130-050544_proclamation_plan.json`
- `.bridges/signals/20260130-050543_missive_assignment.json`
- `.bridges/signals/20260130-050543_proclamation_plan.json`
- `.bridges/signals/20260130-045658_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `scripts/focus`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/focus/focus.py" "$@"
```

### `docs/ops/focus.md`

```
# Focus Ritual

Focus is the shortcut pattern:
- reach a stable level
- then compress the pathway into a single safe ritual

Command:

```bash
./scripts/focus
```

It writes:
- `.substrate/state/focus.json`

It includes:
- health, field Z, budgets, active/next items

The goal is intelligent forgetting:
- once a level is encoded in tooling, you don't need to remember the steps
```

