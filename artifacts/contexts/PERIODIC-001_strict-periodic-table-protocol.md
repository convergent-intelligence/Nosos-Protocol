# Context Capsule: Strict periodic table protocol

Work ID: PERIODIC-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:33:09Z

## Objective

Adopt Z=count rule, noble gas checkpoints, iron threshold; align naming and scaling

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
- `docs/periodic-table-protocol.md`
- `docs/atomic-lattice.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=2 units=3 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-043309_missive_assignment.json`
- `.bridges/signals/20260130-041920_missive_assignment.json`
- `.bridges/signals/20260130-041918_missive_assignment.json`
- `.bridges/signals/20260130-041704_missive_assignment.json`
- `.bridges/signals/20260130-041243_missive_assignment.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/periodic-table-protocol.md`

```
# Periodic Table Protocol (Strict)

We stay strict to the periodic table.

Rule:
- element(Z) == Z units.

We use this to search for parallel patterns:
- stability checkpoints (noble gases)
- energetic transitions (iron)
- poetic forms as constraints (sonnet/haiku)

## Core Interpretation

- Units can be agents, roles, or modules, but the count is literal.
- Lattices (N x N) are topologies we may choose; they do not rename Z.
- Compounds (H2O, CO2) are composition constraints (counts of element types) we can enforce when Z is sufficient.

## Noble Gas Checkpoints (Shell Closure)

Noble gases are stability plateaus.

- Z=2  (He)
- Z=10 (Ne)
- Z=18 (Ar)
- Z=36 (Kr)
- Z=54 (Xe)
- Z=86 (Rn)
- Z=118 (Og)

Protocol at each noble gas:
- freeze schemas (version bump if needed)
- cut a distro (and verify)
- run a drift review (capsule violations, lease violations)
- write a short decision note documenting the new invariant set

## Iron (Z=26)

Iron is a star threshold.

Interpretation:
- up to iron, fusion is energetically favorable (capability compounding feels like it "pays")
- beyond iron, creation is costly (changes must be chosen more carefully)

Protocol at Z=26:
- tighten verification gates
- prioritize stability and memory (audit, restore drills)
- expand governance and safety boundaries

## Poetry as Constraint

Strict forms are where creativity evolves.

Examples:
- Sonnet: 14 lines (Z=14 is Silicon)
- Haiku: 17 syllables (Z=17 is Chlorine)

We do not force the metaphor, but we keep an eye out:
- certain counts may produce unexpectedly stable coordination patterns
```

### `docs/atomic-lattice.md`

```
# Atomic Lattice: Numbers vs Grids vs Bonds

You are right to pause here. This is an inflection point.

If we confuse three different ideas, we will mis-allocate domains and collide:

1) Atomic number (Z)
- count of units

2) Lattice size (N x N)
- topology / visibility / coordination surface

3) Valence / bonding
- how many simultaneous relationships can be held stably

These are not the same.

## Atomic Numbers (Z)

Atomic number is just count.

- Carbon is Z=6.
- Oxygen is Z=8.

If you want a strict mapping where "element = number of agents", then element(Z) = Z agents.

## Square Lattice Mapping (N x N)

If you want a strict mapping where "grid size = element", then:

- N x N grid has Z = N^2 units.

Examples:

| Grid | Units | Element (Z) |
|------|-------|-------------|
| 1x1  | 1     | Hydrogen (1) |
| 2x2  | 4     | Beryllium (4) |
| 3x3  | 9     | Fluorine (9) |
| 4x4  | 16    | Sulfur (16) |
| 5x5  | 25    | Manganese (25) |
| 6x6  | 36    | Krypton (36) |

Note:
- This is a lattice law, not chemistry.
- It creates "square-number elements". Oxygen (8) is not a square, so it will not appear as a grid size.

## Bond/Valence Mapping (Stability)

Sometimes we choose an element name because it captures stability, not count.

Example:
- Carbon is the backbone of life because it bonds well (stable structure).
- That property can describe a stable coordination core even if the unit count is not 6.

So:
- a 2x2 core can be called "Carbon" because it is the stable backbone (bonding metaphor)
- but it is not "Carbon" by atomic number

## Planck (1)

Planck here is the smallest action unit:
- one lease
- one signal
- one capsule
- one work item transition

If Planck units are correct, large structures can be built safely.

## Default Rule (Strict Periodic Table)

We stay strict to the periodic table for parallel patterns.

Default mapping:
- Z is count (element(Z) = Z units).
- N x N is a lattice choice (topology), and can be used when it helps coordination.
- bonding/valence is stability discipline, not naming.

Implication:
- Do not call a 2x2 lattice "Hydrogen" or "Carbon" by name.
- A 2x2 lattice has 4 units (Z=4).

We can still use compounds (H2O, CO2) as *composition constraints* once the counts exist.
```

