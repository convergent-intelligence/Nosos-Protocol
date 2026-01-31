# Phase 0 - Foundation

Goal: establish a safe, documented baseline that can support any future system shape.

## Outcomes

- A single-page system definition (`docs/system-brief.md`)
- A place to record decisions (`docs/decisions/`)
- A minimal shared vocabulary and message format (`.bridges/`)
- A minimal state surface with schema (`.substrate/state/`)
- Phase 0 tooling stubs (registry/state/graph) with schemas (`tools/`)

## Checklist

- [ ] Fill `docs/system-brief.md` (purpose, users, boundaries, risks)
- [ ] Record first decision note in `docs/decisions/` (even if trivial)
- [ ] Update `.bridges/lexicon/core-terms.yaml` with 5-15 terms
- [ ] Update `.bridges/protocols/signal-format.yaml` to match how you will communicate
- [ ] Update `.substrate/constants/constants.yaml` with the first invariants
- [ ] Populate `tools/plan-registry/plans.yaml` with 1-3 initial work items
- [ ] Populate `tools/dependency-graph/graph.yaml` with the first components/dependencies
- [ ] Run `scripts/validate.sh` and fix any failures

Optional (if you want autonomous document/image ingestion from day 0):
- [ ] Run `scripts/autofile init`
- [ ] Drop a few representative files into `inbox/` and run `scripts/autofile scan-inbox`
- [ ] Run `scripts/autofile build-views`
