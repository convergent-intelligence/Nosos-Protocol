# Orchestrator

Orchestrator is a small helper that reads the planning surfaces and prints a suggested execution order.

It is intentionally read-mostly:
- plans live in `tools/plan-registry/plans.yaml`
- state lives in `tools/state-tracker/state.yaml` and `.substrate/state/health.json`
- dependency graph lives in `tools/dependency-graph/graph.yaml`

## Usage

From the scaffold root:

```bash
./scripts/orchestrate status
./scripts/orchestrate next
./scripts/orchestrate next --json
./scripts/orchestrate active
./scripts/orchestrate budgets
./scripts/orchestrate start P1-005 --owner builder
./scripts/orchestrate done P1-005
./scripts/orchestrate assign DEPLOY-001 --owner builder
```

## Notes

This tool uses a minimal YAML subset parser (no external dependencies).
