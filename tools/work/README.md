# Work Tool

Creates work items (plans/issues/bugs/dead ends/stubs) in the registry.

This exists to reduce friction and keep the format consistent.

## Usage

From the scaffold root:

```bash
./scripts/work new bug BUG-001 "Duplicate status lines" --domain scribe --priority high --template
./scripts/work new stub STUB-001 "Idea: OCR pipeline" --domain scribe --priority medium --template
```

What it does:
- appends a new entry to `tools/plan-registry/plans.yaml`
- optionally creates a writeup file under `artifacts/issues/` or `artifacts/stubs/`
