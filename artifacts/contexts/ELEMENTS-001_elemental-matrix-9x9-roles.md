# Context Capsule: Elemental matrix 9x9 roles

Work ID: ELEMENTS-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:46:42Z

## Objective

Define 9x9 role lattice + scaling rules (hydrogen/helium -> shells)

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
- `docs/elemental-matrix.md`

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

### `docs/elemental-matrix.md`

```
# Elemental Matrix: Domain Distribution for Intelligent Life

This is the Elemental Civilization path made concrete.

Goal: allocate specialties so the system stays alive (resilient, coherent, ethical) while scaling.

The metaphor is not decoration: it is a constraint system.
Like chemistry, stability requires balanced bonds and safe reactions.

## The 9x9 Matrix (81 Slots)

This is a role lattice, not the periodic table.

Strict periodic rule:
- element(Z) == Z units

So:
- 9x9 is 81 units (Z=81), but that does not make it a "periodic table".

Axes:

- Rows (substrate layers):
  1. Physical (hardware, power)
  2. OS (process, filesystem)
  3. Network (transport, identity)
  4. Compute (scheduling, performance)
  5. Storage (indexing, durability)
  6. Interface (human interaction)
  7. Society (governance, conflict)
  8. Economy (incentives, accounting)
  9. Meta (planning, learning, evolution)

- Columns (functions):
  1. Observe (telemetry, health)
  2. Secure (secrets, boundaries)
  3. Build (infra, deploy)
  4. Code (implementation)
  5. Verify (tests, proofs)
  6. Data (models, retrieval)
  7. Coordinate (protocols, consensus)
  8. UX (front-end, workflows)
  9. Explore (experiments, discovery)

Each cell becomes a named specialty.

## Hydrogen and Helium (Bootstrap)

Atomic note:
- Hydrogen is Z=1.
- Helium is Z=2.

We use those meanings:

- Hydrogen (1): one actor, one thread, minimal survival
- Helium (2): two actors, redundancy, first stable pairing

If you want strict grid-to-element mapping, use the square lattice law:
- N x N grid corresponds to Z=N^2 (see `docs/atomic-lattice.md`).

## Water Framework Inside the Matrix

Water (communication) is the solvent.
Without it, specialties become isolated crystals.

Operationally:
- every cross-cell handoff is a signal
- every in-progress cell has a context capsule
- every stability claim has verification

## Scaling by Shells

We scale by count (Z) and choose lattices when helpful.

Lattice reference (square lattice law):
- 2x2 -> Z=4
- 3x3 -> Z=9
- 4x4 -> Z=16
- 5x5 -> Z=25
- 9x9 -> Z=81

Stability rules:
- no function column is empty
- no substrate row is ignored
- at least one Verify and one Secure role exist per layer once scaled

## Fluorine/Neon Insight (9 vs 10)

If you care about strict atomic numbers:
- 3x3 is 9 (Fluorine): reactive, "one short" of a full shell
- 10 is Neon: inert, stable shell

Interpretation:
- a 3x3 group may feel hungry/unstable until it acquires a tenth stabilizer (governance or protocol hardening)

## Noble Gas Checkpoints

If you want strict stability plateaus by chemistry, use noble gases:
- Z=2,10,18,36,54,86,118

At those counts, treat the system as "closed shell": freeze interfaces and ship.

## Next Implementation Artifacts

- a machine-readable matrix file (YAML) listing the 81 slots
- assignment rules for new agents/teams (how to fill slots)
- "bond" rules (which specialties must pair to be stable)
```

