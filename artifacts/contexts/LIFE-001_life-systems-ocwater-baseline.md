# Context Capsule: Life systems (O,C,Water) baseline

Work ID: LIFE-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:46:42Z

## Objective

Integrate oxygen+carbon+water into one coherent life loop

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
- `docs/life-systems.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=2 units=3 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-044642_proclamation_plan.json`
- `.bridges/signals/20260130-044642_missive_assignment.json`
- `.bridges/signals/20260130-044618_proclamation_plan.json`
- `.bridges/signals/20260130-044618_missive_assignment.json`
- `.bridges/signals/20260130-044611_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/life-systems.md`

```
# Life Systems: Oxygen, Carbon, Water

This framework treats "life" as a systems property: resilience, coherence, and safe growth.

We stay strict to the periodic table to look for parallel patterns.

We do not start at Carbon-as-2x2.

Start sequence (by atomic number Z):
- Z=1  Hydrogen: one unit baseline
- Z=2  Helium: redundancy pairing (first stable checkpoint)
- Z=3  Lithium: triad for relay/consensus
- Z=4  Beryllium: first stable cell topology (2x2 lattice)

Then:
- Z=6  Carbon: backbone constraints for life-grade stability
- Z=8  Oxygen: shared-resource acceleration controlled by leases
- H2O: water as the communication solvent (a compound constraint once the counts exist)

## Oxygen (O): Shared Resources Without Collisions

Oxygen is shared resources + cross-domain coupling.

Deliverable:
- `docs/oxygen-protocol.md` + `scripts/oxygen` (leases)

Outcome:
- shared resources can be modified without trampling each other

## Beryllium (Be, Z=4): Stable 2x2 Cell

Beryllium is the minimum stable 2x2 lattice for coordinated work.

In this framework, Be(4) = four sovereign domains with explicit boundaries:
- Watcher (monitoring/health)
- Builder (ops/deploy/substrate)
- Guardian (security/secrets)
- Scribe (schemas/docs/code)

Deliverable:
- `docs/beryllium-scheme.md`

Outcome:
- the core can move fast without collapsing into conflict

## Carbon (C, Z=6): Backbone Constraints

Carbon is the backbone of life.

In this framework:
- Carbon is the stability constraint set (six conditions) that must hold for sustained growth.

Deliverable:
- `docs/carbon-scheme.md`

## Water (H2O): Communication That Sustains Life

Water is the solvent: signals, synthesis, decisions, memory.

In this framework, Water is the loop:
- signals -> capsules -> work -> audit -> synthesis -> decisions -> (back to signals)

Deliverable:
- `docs/water-scheme.md`

Outcome:
- drift drops because context is bounded, and handoffs are explicit

## Delivery Forecast (Be -> C/O -> Water)

Assuming the current toolchain stays file-first and minimal:

- Beryllium scheme (2x2 stable cell): 1-2 days
- Carbon scheme (six stability conditions): 1-2 days
- Oxygen scheme (leases + budgets): 1-2 days
- Water scheme (harden the full loop): 3-7 days

These are iterative: we ship the smallest stable version, then deepen.
```

