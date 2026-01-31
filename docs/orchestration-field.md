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
