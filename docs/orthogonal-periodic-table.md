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
