# Context Capsule: Orthogonal periodic table mapping

Work ID: ORTHO-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T05:05:43Z

## Objective

Operationalize Z checkpoints as system capabilities; keep strict periodic rule

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
- `docs/orthogonal-periodic-table.md`
- `docs/periodic-table-protocol.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-050543_proclamation_plan.json`
- `.bridges/signals/20260130-050543_missive_assignment.json`
- `.bridges/signals/20260130-045658_proclamation_plan.json`
- `.bridges/signals/20260130-045658_missive_assignment.json`
- `.bridges/signals/20260130-044940_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/orthogonal-periodic-table.md`

```
# Orthogonal Periodic Table (System Elements)

This is a periodic table *orthogonal* to chemistry.

We keep the periodic table strict (Z is literal), but we interpret each Z as a systems capability checkpoint.

Purpose:
- find parallel patterns (stability plateaus, reactive phases, costly thresholds)
- make "Atomic Autonomy" operational via clear, count-based checkpoints

## Rule

- Z is literal.
- The mapping is conceptual: it does not describe atoms, it describes system capability.

## Checkpoints

- Noble gases (stability plateaus): Z=2,10,18,36,54,86,118
- Iron threshold (cost inflection): Z=26

At checkpoints we ship:
- freeze interfaces (schemas/protocols)
- cut a verified distro
- record a decision note

## The First 18 (Bootstrapping Autonomy)

Each element lists:
- Meaning: the capability added at this count
- Operational surface: what must exist / what we run

Z=1  H  (Existence)
- Meaning: one unit that can execute a full Planck loop
- Operational surface: `./scripts/validate.sh` and a single work item transition

Z=2  He (Redundancy)
- Meaning: first stable pairing; recovery is possible
- Operational surface: `./scripts/backup.sh` + `./scripts/restore.sh` drill

Z=3  Li (Relay)
- Meaning: a third party enables mediation (handoff without collapse)
- Operational surface: signals used for cross-domain handoffs (`./scripts/signal`)

Z=4  Be (Cell)
- Meaning: first stable lattice; domain sovereignty becomes practical
- Operational surface: Be(4) scheme (`docs/beryllium-scheme.md`) + enforced budgets

Z=5  B  (Boundaries)
- Meaning: explicit boundaries around shared resources
- Operational surface: leases required (`./scripts/oxygen claim/release`)

Z=6  C  (Backbone)
- Meaning: stable growth constraints; life-grade coordination
- Operational surface: Carbon constraints (`docs/carbon-scheme.md`)

Z=7  N  (Naming)
- Meaning: shared vocabulary stabilizes reasoning
- Operational surface: lexicon (`.bridges/lexicon/core-terms.yaml`)

Z=8  O  (Oxidation)
- Meaning: shared resources accelerate everything; must be controlled
- Operational surface: oxygen inventory + budgets (`docs/oxygen-protocol.md`, `.substrate/constants/budgets.yaml`)

Z=9  F  (Friction)
- Meaning: guardrails that prevent unsafe speed
- Operational surface: budgets enforced + leases enforced + capsule discipline

Z=10 Ne (Closed Shell)
- Meaning: first stability plateau; interfaces can be frozen and shipped
- Operational surface: `./scripts/build-distro.sh` + `./scripts/verify-distro.sh` + decision record

Z=11 Na (Salt)
- Meaning: defaults that preserve life (new projects don’t regress)
- Operational surface: distro usage docs + install helpers

Z=12 Mg (Ignition)
- Meaning: energy management; continuous operation begins
- Operational surface: daemon/watch loops with safe locks (e.g. `autofile watch-inbox`)

Z=13 Al (Lightweight Structures)
- Meaning: make browsing and manipulation easy without corruption
- Operational surface: deterministic views and safe exports

Z=14 Si (Interfaces)
- Meaning: stable schemas; composability becomes the main design axis
- Operational surface: schema versioning discipline + compatibility notes

Z=15 P  (Memory)
- Meaning: long-term storage of learning
- Operational surface: archaeology + decisions + stubs/dead ends

Z=16 S  (Sanitation)
- Meaning: clean handling of contaminants (secrets, corrupted inputs)
- Operational surface: quarantine + secret invariants + audits

Z=17 Cl (Purification)
- Meaning: reduce drift by enforced process
- Operational surface: capsule budgets + override council calls

Z=18 Ar (Inert Ops)
- Meaning: stable ops surface that doesn’t react badly to change
- Operational surface: runbook completeness + restore drills + health model

## Notes

- This table is a tool for coordination.
- The strictness is the creative constraint: patterns emerge because the rules are fixed.
```

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

Orthogonal mapping:
- `docs/orthogonal-periodic-table.md` maps Z checkpoints to operational capability.

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

