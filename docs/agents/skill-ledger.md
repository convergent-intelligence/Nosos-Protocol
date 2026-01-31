# Skill Ledger (For Gold Later)

This is a planning placeholder for skill profiling and gold attribution.

Principles:
- gold is earned by verified outcomes, not effort
- attribution favors reproducible artifacts (docs, tests, scripts, dashboards)
- rewards should reinforce system health: safety, reliability, clarity, autonomy

## Skill Axes

- Reliability: failure-mode thinking, recovery design, testing
- Observability: useful signals, actionable alerts, runbooks
- Security: secret hygiene, boundaries, audit trails
- Maintainability: interfaces, docs, refactors, onboarding
- Autonomy: idempotence, deterministic behavior, minimal human babysitting

## Evidence Types

- change artifact: decision record, PR/commit, schema change
- operational artifact: runbook, dashboard, alert policy
- verification artifact: tests, checks, scripted validation
- incident artifact: timeline, root cause, prevention work

## Recording Format (Suggested)

Create a short entry per credited outcome:

```yaml
id: "G-20260130-0001"
date: "2026-01-30"
agent: "watcher|builder|guardian|scribe"
outcome: "<what changed in reality>"
evidence:
  - "<path>"
  - "<path>"
points: 0
notes: "<why this matters>"
```
