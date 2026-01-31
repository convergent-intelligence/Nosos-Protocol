# Protocol-First Scaffold

This folder is a reusable directory framework for bootstrapping a new system whose domain is not chosen yet.

The intent is to start with:
- clear places for decisions, state, protocols, and artifacts
- a small Phase 0 foundation (registry/state/graph)
- minimal assumptions about language, runtime, or deployment

## How To Use

1. Copy this folder to the new system location.
2. Fill in `STATUS.md` and `docs/system-brief.md`.
3. Execute Phase 0 in `PHASE-0.md`.
4. Evolve protocols in `.bridges/` as the system becomes defined.

If you are using the four-class agent model, start with:
- `docs/agents/classes.md`
- `.agents/classes.yaml`

## Directory Map

- `docs/` system brief, runbook, decisions
- `.substrate/` ground rules, constants, state, anomalies
- `.agents/` identities/roles/ownership (optional)
- `.bridges/` protocols, lexicon, translations, failures
- `.synthesis/` consensus, disagreements, correlations
- `.pantheon/` external feedback surface (humans/ops/users)
- `.tavern/` informal collaboration space
- `quests/` active work packages
- `artifacts/` completed outputs (tools/protocols/failures)
- `archaeology/` historical record
- `tools/` Phase 0 tooling stubs (registry/state/graph)
- `scripts/` local automation (validate/bootstrap)

Autonomous file organization (optional but implemented here):
- `inbox/` drop zone for arbitrary files
- `store/` content-addressed blobs + derived artifacts
- `units/` human-facing unit folders
- `index/` machine-facing indexes + audit
- `views/` generated views (symlinks)
- `rules/` routing/classification rules

## Conventions

- Prefer plain files over databases early; migrate later when needed.
- Every non-trivial decision gets a short note in `docs/decisions/`.
- Protocols are versioned and explicit; avoid implicit behavior.
- State files are append-only where practical; avoid lossy rewrites.
