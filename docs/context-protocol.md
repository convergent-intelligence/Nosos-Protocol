# Context Protocol: Capsules (Just-Enough Context)

Purpose: prevent drift and "kinetic static" by giving each work item a bounded, explicit context packet.

We do not dump the whole repo. We do not starve the agent. We give exactly what is needed to execute *this* item.

## The Rule

Every work item that moves to `in_progress` should have a context capsule linked from its registry entry.

## Capsule Budget

Hard limits (defaults):
- 1 page of narrative
- up to 5 linked files embedded
- up to 120 lines per embedded file

If the task truly needs more, add a second capsule and explicitly say why.

## Capsule Contents

Required sections:

1) Objective
- what "done" means

2) Boundaries
- what is in scope
- what is out of scope

3) Invariants
- things that must not change

4) Touch Points
- files to edit
- scripts/commands to run

5) Current State
- health snapshot (if available)
- relevant signals (recent)

6) Drift Guards
- 3-5 "do not" statements
- stop conditions (when to ask for clarification)

## File Inclusion Rules

- Prefer:
  - small, authoritative docs
  - schemas and interfaces
  - the exact files expected to change
- Avoid:
  - broad background docs unrelated to the task
  - large log dumps
  - entire directories unless strictly required

## Our Own Standard

We own the context.
If the capsule is wrong, we fix the capsule first.
