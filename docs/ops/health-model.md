# Health Model

The health model is intentionally simple and actionable.

Output is written by `scripts/health.sh` to:
- `.substrate/state/health.json`

## States

- green: no known failures in inbox processing
- yellow: needs attention but not broken
- red: broken; requires intervention

## Current Rules (Phase 0)

- red if `inbox/failed/` has any files
- yellow if any units are quarantined and health is not red
- green otherwise

## Extending

As monitoring grows, add explicit signals:
- index/db integrity
- disk usage thresholds (blob store)
- daemon liveness (watch-inbox)
