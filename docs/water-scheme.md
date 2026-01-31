# Water Scheme: Communication That Sustains Life

Water is the communication solvent.

When carbon is stable, water can flow without becoming fire.

## The Water Loop

```
Signals -> Capsules -> Execution -> Audit -> Synthesis -> Decisions -> Signals
```

Implemented surfaces (today):
- Signals: `.bridges/signals/` + `scripts/signal`
- Capsules: `artifacts/contexts/` + `scripts/context`
- Execution tracking: `tools/plan-registry/plans.yaml` + `scripts/orchestrate`
- Audit: `index/audit.jsonl` (AutoFile) + signal logs

Condensation (synthesis):
- `./scripts/synthesize` writes `.synthesis/consensus/` reports

## What Water Adds Next

1) Condensation (Synthesis)
- create a minimal synthesis surface for:
  - recurring drift patterns
  - repeated dead ends
  - repeated collisions

Implemented:
- `docs/ops/synthesis.md`

2) Precipitation (Decisions)
- ensure decisions are short, versioned, and linked to work items

3) Runoff (Automation)
- move routine loops into daemons safely (watch-inbox, nightly health)

## Water Delivery Forecast

Minimum viable Water (3 days):
- synthesis templates for drift/collisions
- enforced capsule budget and "stop conditions"

Stable Water (7 days):
- metrics for drift (capsule violations, scope expansions, lease violations)
- a weekly synthesis report produced as an artifact

## Exit Criteria (Life)

- work stays within capsule bounds by default
- collisions are rare and recoverable
- when drift happens, it produces a stub/dead_end artifact and a protocol update
