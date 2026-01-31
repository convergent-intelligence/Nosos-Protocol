# Decision 0003: IONOS Target

Date: 2026-01-30
Status: accepted

## Context

ISO upload/attach/boot steps differ across IONOS products (Cloud Server vs VPS vs Dedicated). The build pipeline (and how automated it can be) depends on the target.

## Decision

Chosen target: IONOS Cloud Server.

## Consequences

- Determines the exact UI flow and boot media support.
- Determines whether we should ship ISO vs VM image.

## Next

Once target is chosen:
- update `docs/deploy/ionos-iso.md` with exact steps
- implement DEPLOY-002 against the chosen target
