# Workflow: Orchestrated Systems Work

This is the default workflow for the Agent Systems Framework.

It uses three planning surfaces:
- Plan registry: `tools/plan-registry/plans.yaml`
- State tracker: `tools/state-tracker/state.yaml` + `.substrate/state/health.json`
- Dependency graph: `tools/dependency-graph/graph.yaml`

And one coordination surface:
- Signals: `.bridges/signals/` (use the schema in `.bridges/protocols/signal-format.yaml`)

Helper:
- `./scripts/signal` writes signals as JSON files into `.bridges/signals/`

## The Loop

1. Assess
   - run `./scripts/health.sh`
   - run `./scripts/field status` (orchestrating field)
   - check `./scripts/orchestrate status`
   - optional: `./scripts/synthesize` (condense signals)

Shortcut:
- `./scripts/focus` (writes `.substrate/state/focus.json`)
2. Generate candidates
   - check `./scripts/orchestrate next`
3. Decide
   - record non-trivial choices in `docs/decisions/`
4. Assign with just-enough context
   - `./scripts/orchestrate assign <plan-id> --owner <who>`
   - this generates a context capsule and emits a missive
5. Execute
   - implement changes; keep invariants

Lease rule for shared resources:
- before changing a shared resource, claim a lease with `./scripts/oxygen claim ...`
- see `docs/oxygen-protocol.md`

Atomic autonomy guardrail:
- check concurrency budgets: `./scripts/orchestrate budgets`
- `assign` enforces `max_in_progress_per_domain` from `.substrate/constants/budgets.yaml`
- budget override requires `--override --reason` and emits a council_call
5. Verify
   - `./scripts/validate.sh`
   - `./scripts/health.sh`
6. Update plan state
   - `./scripts/orchestrate start <plan-id>` and `./scripts/orchestrate done <plan-id>`
6. Package (when needed)
   - `./scripts/build-distro.sh` and `./scripts/verify-distro.sh`

## Domain Handshakes

When work crosses domains (watcher/builder/guardian/scribe/gems), write a signal:

- proclamation: broadcast status
- missive: request a specific action
- council_call: request a decision

Store signals as files under `.bridges/signals/`.
