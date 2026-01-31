# Tracking: Plans, Issues, Bugs, Dead Ends, Stubs

This framework uses the same item system to track all work and learning.

## Single Queue

The single queue is:
- `tools/plan-registry/plans.yaml`

Each entry is a "work item" with a `kind`:
- `plan` (intended work)
- `issue` (problem to solve, may not be a bug)
- `bug` (incorrect behavior)
- `dead_end` (path tried that should not be repeated)
- `stub` (cognitive stub: incomplete thought, hypothesis, TODO for future inquiry)

## Where Details Live

- The registry entry is an index card: status, owner, links.
- The body lives in durable artifacts:
  - `artifacts/issues/` for issue/bug writeups
  - `artifacts/stubs/` for stubs and dead ends
  - `.substrate/anomalies/` for runtime weirdness
  - `docs/decisions/` for irreversible choices

## Workflow

1. Create a work item in `tools/plan-registry/plans.yaml`.
2. Write the narrative in an artifact file and link it from the item.
3. Generate a context capsule and link it from the item:
   - `./scripts/context make <id>`
3. Use orchestrator to move states:
   - `./scripts/orchestrate start <id> --owner <name>`
   - `./scripts/orchestrate done <id>`
   - `./scripts/orchestrate block <id>`
4. Emit a signal when a dead end is discovered.

Helper:
- `./scripts/work new ...` creates a registry entry and can generate a writeup template.

Templates:
- `docs/templates/bug.md`
- `docs/templates/issue.md`
- `docs/templates/dead-end.md`
- `docs/templates/stub.md`

Context:
- Protocol: `docs/context-protocol.md`
- Generator: `./scripts/context`
