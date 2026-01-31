# Decision 0001: Adopt Protocol-First Scaffold

Date: 2026-01-30
Status: accepted

## Context

The system domain is not yet chosen. We need a stable, low-assumption starting point that supports discovery, feedback, and evolution without premature architecture.

## Decision

Start from a protocol-first directory scaffold:
- explicit locations for protocols, state, decisions, and artifacts
- file-first Phase 0 tooling (plan registry, state tracker, dependency graph)
- minimal constraints on language/runtime/deployment

## Consequences

- Faster onboarding: newcomers can find the same kinds of information in the same places.
- Reduced ambiguity: decisions and message formats are recorded, not implied.
- Some overhead: maintaining lightweight files and schemas is required.

## Alternatives Considered

- Start coding immediately and retrofit structure later.
- Adopt a language-specific layout up front.
