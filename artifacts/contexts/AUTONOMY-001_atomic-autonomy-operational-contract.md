# Context Capsule: Atomic Autonomy operational contract

Work ID: AUTONOMY-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:46:18Z

## Objective

Make autonomy enforceable: budgets, leases, capsules, signals

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
- `docs/atomic-autonomy.md`
- `scripts/orchestrate`
- `docs/oxygen-protocol.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=2 units=3 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-044611_proclamation_plan.json`
- `.bridges/signals/20260130-044611_missive_assignment.json`
- `.bridges/signals/20260130-044604_proclamation_plan.json`
- `.bridges/signals/20260130-044556_proclamation_plan.json`
- `.bridges/signals/20260130-044119_proclamation_autonomy.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

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

- leases for shared resources (`scripts/oxygen`)
- budgets for concurrency (in_progress per domain)

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

### `scripts/orchestrate`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/orchestrator/orchestrator.py" "$@"
```

### `docs/oxygen-protocol.md`

```
# Oxygen Protocol: Resource + Domain Distribution

Oxygen is the challenge because it accelerates everything.

In systems terms:
- oxygen = shared resources + cross-domain coupling
- too little oxygen = stagnation
- too much oxygen = conflict, drift, and burning the system down

This protocol prevents "stepping on ourselves" while still enabling fast reactions.

## 1) Domain Sovereignty (Primary Constraint)

We do not coordinate by chatting. We coordinate by boundaries.

Domains (owners):
- watcher: health, monitoring, incident response surfaces
- builder: runtime substrate, deploy, backups, ops automation
- guardian: secrets, access boundaries, quarantine policy
- scribe: schemas, code quality, documentation, planning surfaces
- gems: UX contracts and interfaces (front-end)

Rule:
- If you touch another domain's core surface, you need a handshake signal.

## 2) Shared Resource Types (Oxygen Inventory)

These are the things that cause collisions.

We keep this list at 8 on purpose (oxygen is 8):

1. schema resources
   - `tools/plan-registry/schema.yaml`, `.bridges/protocols/signal-format.yaml`, unit conventions
2. storage resources
   - `store/blobs/`, `store/derived/`, backups
3. index resources
   - `index/autofile.sqlite`, migrations, rebuild procedures
4. execution resources
   - daemons, cron jobs, long-running processes, lock files
5. deployment resources
   - distro build, ISO/image build, install scripts
6. identity resources
   - users, permissions, SSH access model (no keys baked into images)
7. policy resources
   - secret handling invariants, quarantine rules, access boundaries
8. coordination resources
   - plan registry semantics, assignment workflow, signal conventions

## 3) The Mechanism: Leases (Claim/Release)

We use short-lived leases to avoid collisions.

- A lease is a file under `.substrate/state/leases/`.
- A lease has:
  - resource id (string)
  - owner
  - domain
  - ttl (seconds)
  - created_at / expires_at

Rule:
- Before changing a shared resource, claim a lease.
- When done, release.
- If blocked, raise a council_call.

## 4) The Mechanism: Context Capsules (Right-Size Inputs)

Collisions also happen when agents carry too much context and take action outside scope.

Rule:
- Every in_progress work item gets a context capsule.
- Use `./scripts/orchestrate assign <id> --owner <who>`.

## 5) The Mechanism: Signals (Explicit Handoffs)

Rule:
- Cross-domain handoff must be a missive or council_call.
- Evidence is the capsule path and the exact files.

## 6) The Balance Law

We balance oxygen with three budgets:

- change budget: how many shared resources can be leased concurrently
- risk budget: how much can change without verification
- attention budget: how many in_progress items can exist per domain

Defaults:
- max 2 leases per domain at once
- max 2 in_progress per domain at once (hard stop unless council_call)

## 7) Failure Modes

- lease hoarding: leases never released
  - fix: TTL expiry + audit

- shadow edits: changes without lease or without capsule
  - fix: reject/undo; create a dead_end artifact explaining why

- ambiguous ownership: unclear domain boundaries
  - fix: update `docs/agents/classes.md` and lexicon; then proceed
```

