# Context Capsule: Quantum overlay + convergence

Work ID: QUANTUM-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T05:05:43Z

## Objective

Add probabilistic overlay (stubs/issues with confidence) that collapses via decisions; keep core deterministic

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
- `docs/quantum-convergence.md`
- `docs/atomic-autonomy.md`

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

### `docs/quantum-convergence.md`

```
# Quantum Convergence: When to Model Reality Differently

We can treat the system as "quantum" without turning it into mysticism.

Operational meaning:
- quantum = we explicitly represent uncertainty as distributions
- measurement = we commit a decision and collapse uncertainty into a chosen state

## Recommendation

Use a two-layer model:

1) Classical core (deterministic)
- files, schemas, leases, budgets, and audits are deterministic
- execution is reproducible

2) Quantum overlay (probabilistic)
- multiple hypotheses and plans can exist simultaneously
- we track confidence and expected outcomes
- we collapse only at decision/commit boundaries

This gives convergence:
- exploration stays probabilistic
- production execution stays deterministic

## Quantum Primitives (Mapped to Our Tools)

- Superposition (many plausible worlds)
  - stubs + issues represent alternative hypotheses

- Amplitude (weight)
  - store confidence as a number (0..1) in the writeup

- Measurement (collapse)
  - a decision record or a council_call resolution
  - a work item moved to in_progress/done

- Entanglement (coupling)
  - shared resources
  - operationally: oxygen leases + budgets

## Where Quantum Stops

Quantum does not apply to:
- blob immutability
- audit logs
- lease semantics
- schema versions

Those stay classical.

## How to Operationalize Next

Add one new practice:
- every stub/issue includes:
  - confidence
  - expected impact
  - what measurement would change the weight

Then:
- the "knower" uses synthesis to update weights
- the council uses thresholds to decide when to collapse
```

### `docs/atomic-autonomy.md`

```
# Atomic Autonomy (Goal #1)

Atomic Autonomy means the system can grow without trampling itself.

Operationally:
- each domain can execute and recover independently
- shared resources are touched only through explicit protocols
- coordination is explicit, bounded, and auditable

This is not a vibe. It is a set of enforceable rules.

## The Atomic Unit (Planck)

The smallest actionable unit is one of:

- a work item state transition (pending -> in_progress -> done)
- a context capsule generation
- a signal (missive/proclamation/council_call)
- a resource lease claim/release

If Planck units are correct, large structures can be built safely.

## Autonomy Contracts

### Domain Autonomy Contract

For each domain (watcher/builder/guardian/scribe/gems):

- a clear owned surface (docs/scripts it controls)
- a way to verify health (health signal or check)
- a way to recover (runbook/restore path)
- a way to refuse cross-domain interference (handshake required)

### Tool Autonomy Contract

Any tool we add should be:

- idempotent (safe to run twice)
- auditable (writes an event or artifact)
- bounded (does not mutate unrelated state)
- versioned at interfaces (schemas/protocols)

## Anti-Drift Contract

- every in_progress item has a context capsule
- every cross-domain handoff is a signal with evidence (capsule + files)
- if more context is needed, create a stub explaining why

## Collision Prevention

- leases for shared resources (`scripts/oxygen`) with per-domain lease budgets
- budgets for concurrency (in_progress per domain) enforced by `scripts/orchestrate assign`
  - configured in `.substrate/constants/budgets.yaml`

## When Phases Are Enough vs When Revolution Is Required

Phase change:
- incremental additions
- no breaking schema changes
- migrations are optional

Revolution:
- schema/layout breakage (unit.yaml, index schema, store layout)
- a new coordination physics (new lease/handshake model)
- a new substrate (deployment/runtime change)

Rule:
- revolutions must be explicit work items and produce a decision record
```

