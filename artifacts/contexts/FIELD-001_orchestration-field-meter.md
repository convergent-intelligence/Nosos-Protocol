# Context Capsule: Orchestration field meter

Work ID: FIELD-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:56:58Z

## Objective

Make periodic Z checkpoints measurable and written to .substrate/state/field.json

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
- `docs/orchestration-field.md`
- `scripts/field`
- `tools/field/orthogonal-table.json`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=2 units=3 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-044940_proclamation_plan.json`
- `.bridges/signals/20260130-044940_missive_assignment.json`
- `.bridges/signals/20260130-044643_proclamation_plan.json`
- `.bridges/signals/20260130-044642_missive_assignment.json`
- `.bridges/signals/20260130-044642_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/orchestration-field.md`

```
# Orchestration Field

The periodic table is not just a metaphor. It is a field.

Field = a set of constraints + potentials that shape what work is safe and what work is timely.

We stay strict to the periodic table (Z is literal), but interpret Z as *system capability checkpoints*.

## Components

- The Table (the field definition)
  - `docs/orthogonal-periodic-table.md`
  - `tools/field/orthogonal-table.json` (machine-readable)

- The Knower (the observer)
  - `.pantheon/observers/knower.md`

- The Meter (the measurement)
  - `scripts/field`
  - `.substrate/state/field.json`

## How the Field Orchestrates

- The field does not command.
- The field gates:
  - what we assign next
  - how much concurrency we allow
  - when we freeze interfaces and ship

## Field Rules

1) Z is literal
- a checkpoint is only achieved when its checks are true

2) Consecutive Z matters
- the current Z is the highest consecutive checkpoint achieved from Z=1 upward

3) Noble gas plateaus are release rituals
- when reaching Z=2/10/18/... we freeze and ship (distro+verify+decision)

4) Iron threshold is governance tightening
- at Z=26 we increase verification and reduce uncontrolled change

## Usage

```bash
./scripts/field status
./scripts/field write
```
```

### `scripts/field`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/field/field.py" "$@"
```

### `tools/field/orthogonal-table.json`

```
{
  "version": "0.1",
  "elements": [
    {
      "z": 1,
      "symbol": "H",
      "name": "Existence",
      "checks": [
        {"kind": "file_exists", "path": "scripts/validate.sh"},
        {"kind": "file_exists", "path": "tools/plan-registry/plans.yaml"}
      ]
    },
    {
      "z": 2,
      "symbol": "He",
      "name": "Redundancy",
      "checks": [
        {"kind": "file_exists", "path": "scripts/backup.sh"},
        {"kind": "file_exists", "path": "scripts/restore.sh"}
      ]
    },
    {
      "z": 3,
      "symbol": "Li",
      "name": "Relay",
      "checks": [
        {"kind": "file_exists", "path": "scripts/signal"},
        {"kind": "file_exists", "path": ".bridges/protocols/signal-format.yaml"}
      ]
    },
    {
      "z": 4,
      "symbol": "Be",
      "name": "Cell",
      "checks": [
        {"kind": "file_exists", "path": "docs/beryllium-scheme.md"},
        {"kind": "file_exists", "path": "scripts/orchestrate"}
      ]
    },
    {
      "z": 5,
      "symbol": "B",
      "name": "Boundaries",
      "checks": [
        {"kind": "file_exists", "path": "scripts/oxygen"},
        {"kind": "file_exists", "path": "docs/oxygen-protocol.md"}
      ]
    },
    {
      "z": 6,
      "symbol": "C",
      "name": "Backbone",
      "checks": [
        {"kind": "file_exists", "path": "docs/carbon-scheme.md"},
        {"kind": "file_exists", "path": "docs/context-protocol.md"}
      ]
    },
    {
      "z": 7,
      "symbol": "N",
      "name": "Naming",
      "checks": [
        {"kind": "file_exists", "path": ".bridges/lexicon/core-terms.yaml"}
      ]
    },
    {
      "z": 8,
      "symbol": "O",
      "name": "Oxidation",
      "checks": [
        {"kind": "file_exists", "path": ".substrate/constants/budgets.yaml"},
        {"kind": "file_exists", "path": "docs/atomic-autonomy.md"}
      ]
    },
    {
      "z": 9,
      "symbol": "F",
      "name": "Friction",
      "checks": [
        {"kind": "file_exists", "path": "scripts/context"},
        {"kind": "file_exists", "path": "tools/context/context.py"}
      ]
    },
    {
      "z": 10,
      "symbol": "Ne",
      "name": "Closed Shell",
      "checks": [
        {"kind": "file_exists", "path": "scripts/build-distro.sh"},
        {"kind": "file_exists", "path": "scripts/verify-distro.sh"},
        {"kind": "glob_exists", "pattern": "dist/agent-systems-framework-*.tar.gz"}
      ]
    },
    {
      "z": 11,
      "symbol": "Na",
      "name": "Defaults",
      "checks": [
        {"kind": "file_exists", "path": "scripts/deploy/install-asf.sh"},
        {"kind": "file_exists", "path": "docs/deploy/image-spec.md"}
      ]
    },
    {
      "z": 12,
      "symbol": "Mg",
      "name": "Ignition",
      "checks": [
        {"kind": "file_exists", "path": "scripts/autofile"}
      ]
    }
  ],
  "noble_gases": [2, 10, 18, 36, 54, 86, 118],
  "iron_threshold": 26
}
```

