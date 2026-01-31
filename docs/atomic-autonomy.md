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
