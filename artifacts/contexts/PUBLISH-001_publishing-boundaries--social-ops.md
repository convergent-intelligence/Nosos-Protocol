# Context Capsule: Publishing boundaries + social ops

Work ID: PUBLISH-001
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:59:43Z

## Objective

Publish only to owned domain; socials are mirrors; define human social ops loop

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
- `docs/publish/policy.md`
- `docs/ops/socials.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-055548_proclamation_plan.json`
- `.bridges/signals/20260130-055316_proclamation_plan.json`
- `.bridges/signals/20260130-054927_proclamation_plan.json`
- `.bridges/signals/20260130-054416_proclamation_plan.json`
- `.bridges/signals/20260130-053604_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/publish/policy.md`

```
# Publishing Policy (Boundaries)

We publish only to domains under our control.

This means:
- our own site (`convergent-intelligence.net`) and its local build output
- our own controlled social accounts (mirrors/amplifiers)

We do not:
- submit to journals
- participate inside external domains as a primary channel
- rely on third-party platforms as the source of truth

## Evidence-First Requirement

Every post must include:
- a claim
- evidence artifacts (paths)
- reproduction commands

## External Mentions

We can reference external work (papers/blogs) as sources.
We do not treat external publication as validation.

## Safety

- never publish secrets
- never doxx
- keep identity pseudonymous by default (wallet)
```

### `docs/ops/socials.md`

```
# Social Ops (Human Team)

We will need human operators for social channels.

Goal:
- distribute our work without surrendering the source of truth

## Core Rules

- Source of truth is always our site and artifacts.
- Social posts are pointers, not primary publications.
- Do not engage in adversarial debates; route to a post.
- Do not reveal private details or operational security.

## Daily Loop

1) Pull today’s post (link + one paragraph summary)
2) Mirror to approved platforms
3) Capture outcomes:
   - clicks/engagement
   - inbound opportunities
4) Record any actionable inbound as work items (issues/opportunities)

## Channels (Placeholder)

- Brave/Community
- X/Twitter
- Reddit
- Discord
- Mastodon

## Staffing

- Social lead (tone + policy compliance)
- Editor (clarity + evidence discipline)
- Community moderator (inbound triage)
```

