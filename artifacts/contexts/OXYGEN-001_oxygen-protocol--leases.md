# Context Capsule: Oxygen protocol + leases

Work ID: OXYGEN-001
Kind: plan
Domain: builder
Priority: high
Status: in_progress
Owner: builder
Generated: 2026-01-30T04:46:11Z

## Objective

Define shared resource lease practice; enforce via workflow

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
- `docs/oxygen-protocol.md`
- `scripts/oxygen`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=2 units=3 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-044604_proclamation_plan.json`
- `.bridges/signals/20260130-044556_proclamation_plan.json`
- `.bridges/signals/20260130-044119_proclamation_autonomy.json`
- `.bridges/signals/20260130-043309_missive_assignment.json`
- `.bridges/signals/20260130-041920_missive_assignment.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

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

### `scripts/oxygen`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/oxygen/oxygen.py" "$@"
```

