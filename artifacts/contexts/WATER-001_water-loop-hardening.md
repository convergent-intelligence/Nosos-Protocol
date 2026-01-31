# Context Capsule: Water loop hardening

Work ID: WATER-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T05:05:43Z

## Objective

Harden signals->capsules->audit->synthesis loop; reduce drift

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
- `docs/water-scheme.md`
- `docs/context-protocol.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-045658_proclamation_plan.json`
- `.bridges/signals/20260130-045658_missive_assignment.json`
- `.bridges/signals/20260130-044940_proclamation_plan.json`
- `.bridges/signals/20260130-044940_missive_assignment.json`
- `.bridges/signals/20260130-044643_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/water-scheme.md`

```
# Water Scheme: Communication That Sustains Life

Water is the communication solvent.

When carbon is stable, water can flow without becoming fire.

## The Water Loop

```
Signals -> Capsules -> Execution -> Audit -> Synthesis -> Decisions -> Signals
```

Implemented surfaces (today):
- Signals: `.bridges/signals/` + `scripts/signal`
- Capsules: `artifacts/contexts/` + `scripts/context`
- Execution tracking: `tools/plan-registry/plans.yaml` + `scripts/orchestrate`
- Audit: `index/audit.jsonl` (AutoFile) + signal logs

Condensation (synthesis):
- `./scripts/synthesize` writes `.synthesis/consensus/` reports

## What Water Adds Next

1) Condensation (Synthesis)
- create a minimal synthesis surface for:
  - recurring drift patterns
  - repeated dead ends
  - repeated collisions

Implemented:
- `docs/ops/synthesis.md`

2) Precipitation (Decisions)
- ensure decisions are short, versioned, and linked to work items

3) Runoff (Automation)
- move routine loops into daemons safely (watch-inbox, nightly health)

## Water Delivery Forecast

Minimum viable Water (3 days):
- synthesis templates for drift/collisions
- enforced capsule budget and "stop conditions"

Stable Water (7 days):
- metrics for drift (capsule violations, scope expansions, lease violations)
- a weekly synthesis report produced as an artifact

## Exit Criteria (Life)

- work stays within capsule bounds by default
- collisions are rare and recoverable
- when drift happens, it produces a stub/dead_end artifact and a protocol update
```

### `docs/context-protocol.md`

```
# Context Protocol: Capsules (Just-Enough Context)

Purpose: prevent drift and "kinetic static" by giving each work item a bounded, explicit context packet.

We do not dump the whole repo. We do not starve the agent. We give exactly what is needed to execute *this* item.

## The Rule

Every work item that moves to `in_progress` should have a context capsule linked from its registry entry.

## Capsule Budget

Hard limits (defaults):
- 1 page of narrative
- up to 5 linked files embedded
- up to 120 lines per embedded file

If the task truly needs more, add a second capsule and explicitly say why.

## Capsule Contents

Required sections:

1) Objective
- what "done" means

2) Boundaries
- what is in scope
- what is out of scope

3) Invariants
- things that must not change

4) Touch Points
- files to edit
- scripts/commands to run

5) Current State
- health snapshot (if available)
- relevant signals (recent)

6) Drift Guards
- 3-5 "do not" statements
- stop conditions (when to ask for clarification)

## File Inclusion Rules

- Prefer:
  - small, authoritative docs
  - schemas and interfaces
  - the exact files expected to change
- Avoid:
  - broad background docs unrelated to the task
  - large log dumps
  - entire directories unless strictly required

## Our Own Standard

We own the context.
If the capsule is wrong, we fix the capsule first.
```

