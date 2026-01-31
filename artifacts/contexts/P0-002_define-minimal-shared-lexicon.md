# Context Capsule: Define minimal shared lexicon

Work ID: P0-002
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T03:58:36Z

## Objective

Add 5-15 terms that reduce early ambiguity

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
- `.bridges/lexicon/core-terms.yaml`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=1 units=2 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-035647_missive_assignment.json`
- `.bridges/signals/20260130-035536_missive_assignment.json`
- `.bridges/signals/20260130-035536_proclamation_plan.json`
- `.bridges/signals/20260130-035509_missive_assignment.json`
- `.bridges/signals/20260130-034638_council_call_deploy.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `.bridges/lexicon/core-terms.yaml`

```
version: 0.1

terms:
  - term: "system"
    meaning: "The thing being built/operated; scope defined in docs/system-brief.md"
  - term: "protocol"
    meaning: "A documented interaction pattern with explicit inputs/outputs"
  - term: "signal"
    meaning: "A structured message following .bridges/protocols/signal-format.yaml"
  - term: "artifact"
    meaning: "A durable output (tool, doc, schema, report) stored under artifacts/"
  - term: "phase 0"
    meaning: "Foundation work that makes later work safer and faster"

  - term: "domain"
    meaning: "A bounded area of authority owned by a class (watcher/builder/guardian/scribe)"

  - term: "handoff"
    meaning: "An explicit transfer of responsibility across domains, recorded as a signal"

  - term: "quarantine"
    meaning: "A holding area for risky or low-confidence items requiring review"

  - term: "work item"
    meaning: "A tracked unit of work in tools/plan-registry/plans.yaml (plan/issue/bug/dead_end/stub)"

  - term: "context capsule"
    meaning: "A bounded task context packet generated under artifacts/contexts/ and linked from a work item"

  - term: "dead end"
    meaning: "A path tried that should not be repeated; record the why and the guardrail"

  - term: "stub"
    meaning: "A cognitive placeholder: a hypothesis or incomplete thought worth preserving"

  - term: "distro"
    meaning: "A shippable tarball of the framework scaffold excluding user data by default"

  - term: "iso"
    meaning: "A bootable image used to install or demo a server environment"

  - term: "quarantine marker"
    meaning: "A file under quarantine/ describing why a unit was quarantined"
```

