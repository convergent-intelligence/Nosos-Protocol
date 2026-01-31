# Focus Modes (Levels as Weights)

Focus levels are not a feature. They are an operating mode.

Operationally:
- a focus level is a vector of weights that changes how we respond to the same facts
- the tools are constant; the mode changes prioritization and thresholds

## The Model

Weights:
- safety: avoid collisions and irreversible changes
- verify: prefer checks, proofs, reproducibility
- execute: move work items forward
- explore: create stubs, test hypotheses, gather evidence

The level is a named preset of these weights.

## Levels (Default Presets)

- 1 stabilize: stop bleeding, reduce entropy
- 2 operate: normal build mode
- 3 translate: turn state into the next concrete action
- 4 explore: increase hypothesis generation and measurement
- 5 ship: release ritual (freeze, verify, package)

Extended presets may use Z checkpoints directly:
- 10 closed_shell: ship ritual
- 12 ignition: execute-forward while watching locks/health
- 17 purification: clean drift, review quarantine, reduce entropy
- 18 inert_ops: ship + restore drill + runbook

Presets live in:
- `tools/focus/levels.json`

## How To Use

- `./scripts/focus status --level 2`
- `./scripts/focus route --level 3`
- `./scripts/focus explain --level 10`

Or set once for the session:

```bash
export ASF_FOCUS_LEVEL=3
./scripts/focus route
```

## Relation to Gold/Goals

Treat the weights as how we intelligently challenge a work item:
- raise safety/verify when changes are risky (deployment, schema)
- raise explore when uncertainty is high (issues/stubs)
- raise execute when the system is stable and you want throughput
