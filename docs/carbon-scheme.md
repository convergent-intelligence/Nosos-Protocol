# Carbon Scheme (C, Z=6): Backbone Constraints

Carbon is Z=6.

We stay strict: Carbon is not a 2x2.
The 2x2 cell is Be(4): `docs/beryllium-scheme.md`.

Carbon is the backbone constraint set: six conditions that must hold for life-grade stability.

## The Six Stability Conditions (C = 6)

These six conditions must hold for sustained growth:

1. Sovereignty: domain ownership is explicit
2. Leases: shared resources require `oxygen` leases
3. Capsules: every in_progress item has bounded context
4. Signals: cross-domain handoffs are explicit
5. Verification: validate/health gates exist
6. Memory: audit + artifacts preserve learning

## What Carbon Adds Beyond Be(4)

Be(4) gives domains.

C(6) adds two backbone capabilities:
- synthesis discipline (condense signals into decisions)
- governance discipline (decisions evolve by protocol, not impulse)

## Domain Surfaces (What Each Owns)

Watcher owns:
- `docs/ops/health-model.md`
- `scripts/health.sh`
- runbooks and incident templates

Builder owns:
- deploy + image pipelines (`docs/deploy/*`, `scripts/deploy/*`)
- backup/restore (`scripts/backup.sh`, `scripts/restore.sh`)

Guardian owns:
- secret handling and quarantine invariants (`docs/security/secret-handling.md`)
- oxygen policy constraints for sensitive resources

Scribe owns:
- schemas/interfaces (plan registry schema, signal schema, unit.yaml conventions)
- documentation pathways and tool UX (CLI outputs)

## The Anti-Collision Contract

Rule 1: lease before shared changes
- Any change to a shared resource requires an oxygen lease.
- Tool: `scripts/oxygen`

Shared resource examples:
- schema: `tools/plan-registry/schema.yaml`, `.bridges/protocols/signal-format.yaml`
- deployment: `scripts/build-distro.sh`, `scripts/deploy/*`
- state: `.substrate/state/*`

Rule 2: capsule for every active item
- Every `in_progress` work item must have a context capsule.
- Tool: `scripts/orchestrate assign` (preferred)

Rule 3: signal for cross-domain handoffs
- Handoffs are missives with evidence (capsule path, files).

## Delivery Forecast (Carbon)

Minimum viable Carbon (1-2 days):
- domain boundaries documented
- leases + assignment + capsules used for all shared work

Stable Carbon (2-4 days):
- enforced budgets (max in_progress per domain)
- recurring review: weekly drift audit and collision audit

## Exit Criteria (Ready For Water)

- At least one work item per domain can run in parallel without collisions.
- Shared resources have leases during edits.
- Cross-domain work produces signals with capsules.
