# Context Capsule: Beryllium (Z=4) 2x2 cell operating model

Work ID: CARBON-001
Kind: plan
Domain: scribe
Priority: high
Status: in_progress
Owner: scribe
Generated: 2026-01-30T04:46:42Z

## Objective

Strict periodic: 2x2 is Z=4 (Be). Define stable 2x2 domain model + exit criteria for Carbon/Water

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
- `docs/beryllium-scheme.md`
- `docs/atomic-lattice.md`
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
- `.bridges/signals/20260130-044618_proclamation_plan.json`
- `.bridges/signals/20260130-044618_missive_assignment.json`
- `.bridges/signals/20260130-044611_proclamation_plan.json`
- `.bridges/signals/20260130-044611_missive_assignment.json`
- `.bridges/signals/20260130-044604_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/beryllium-scheme.md`

```
# Beryllium Scheme (Be, Z=4): Stable 2x2 Cell

Beryllium is Z=4.

This is the first stable cell topology: a 2x2 lattice.

## The 2x2

```
Watcher   | Builder
----------+--------
Guardian  | Scribe
```

Each cell is sovereign in its domain.

## Purpose

Be(4) exists so oxygen does not become fire.
It creates explicit domain boundaries before shared resources accelerate.

## Exit Criteria (Ready For Carbon)

- At least one work item per domain can run in parallel without collisions.
- Cross-domain work is done by missives with capsules.
- Shared resources are protected by leases when edited.
```

### `docs/atomic-lattice.md`

```
# Atomic Lattice: Numbers vs Grids vs Bonds

You are right to pause here. This is an inflection point.

If we confuse three different ideas, we will mis-allocate domains and collide:

1) Atomic number (Z)
- count of units

2) Lattice size (N x N)
- topology / visibility / coordination surface

3) Valence / bonding
- how many simultaneous relationships can be held stably

These are not the same.

## Atomic Numbers (Z)

Atomic number is just count.

- Carbon is Z=6.
- Oxygen is Z=8.

If you want a strict mapping where "element = number of agents", then element(Z) = Z agents.

## Square Lattice Mapping (N x N)

If you want a strict mapping where "grid size = element", then:

- N x N grid has Z = N^2 units.

Examples:

| Grid | Units | Element (Z) |
|------|-------|-------------|
| 1x1  | 1     | Hydrogen (1) |
| 2x2  | 4     | Beryllium (4) |
| 3x3  | 9     | Fluorine (9) |
| 4x4  | 16    | Sulfur (16) |
| 5x5  | 25    | Manganese (25) |
| 6x6  | 36    | Krypton (36) |

Note:
- This is a lattice law, not chemistry.
- It creates "square-number elements". Oxygen (8) is not a square, so it will not appear as a grid size.

## Bond/Valence Mapping (Stability)

Sometimes we choose an element name because it captures stability, not count.

Example:
- Carbon is the backbone of life because it bonds well (stable structure).
- That property can describe a stable coordination core even if the unit count is not 6.

So:
- a 2x2 core can be called "Carbon" because it is the stable backbone (bonding metaphor)
- but it is not "Carbon" by atomic number

## Planck (1)

Planck here is the smallest action unit:
- one lease
- one signal
- one capsule
- one work item transition

If Planck units are correct, large structures can be built safely.

## Default Rule (Strict Periodic Table)

We stay strict to the periodic table for parallel patterns.

Default mapping:
- Z is count (element(Z) = Z units).
- N x N is a lattice choice (topology), and can be used when it helps coordination.
- bonding/valence is stability discipline, not naming.

Implication:
- Do not call a 2x2 lattice "Hydrogen" or "Carbon" by name.
- A 2x2 lattice has 4 units (Z=4).

We can still use compounds (H2O, CO2) as *composition constraints* once the counts exist.
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

