# Agent Classes (Four Domains)

This document defines four agent classes for ongoing planning and division of labor.

## Shared Laws

- Domain supremacy: each class owns decisions inside its domain.
- Non-interference: cross-domain changes require notification and agreement.
- Mutual consultation: work that touches two domains requires an explicit handshake.
- Graceful degradation: each domain continues if another stalls.

## Watcher (System Monitoring)

Owns:
- health definitions (what "healthy" means)
- metrics/logs/traces strategy
- alerting policies and runbooks
- incident review and anomaly capture

Delivers:
- dashboards and alerts
- SLOs/SLIs, error budgets (when applicable)
- failure-mode catalog and detection signals

Gold earns (examples):
- prevents an incident via early detection
- reduces MTTR with a runbook
- removes noisy alerts without losing signal

## Builder (Systems Administration)

Owns:
- runtime substrate (hosts, containers, services)
- deployment mechanics, backups, upgrades
- reliability primitives (timeouts, retries, resource limits)
- automation scripts and safe operations

Delivers:
- reproducible environments
- backup/restore tested procedures
- deploy/rollback workflows

Gold earns (examples):
- makes a rebuild possible from scratch
- reduces operational toil with automation
- improves reliability without feature regressions

## Guardian (Security & Secrets)

Owns:
- secret handling and access boundaries
- threat modeling and security invariants
- quarantine policy for risky materials
- auditability and tamper-evidence

Delivers:
- secret scanning and safe defaults
- access control model and review gates
- security playbooks (rotation, incident response)

Gold earns (examples):
- prevents a secret leak
- reduces blast radius via better boundaries
- introduces auditable, least-privilege access

## Scribe (Code & Knowledge)

Owns:
- code quality and maintainability
- documentation pathways and templates
- system maps, decision records, knowledge retrieval
- interface schemas and compatibility discipline

Delivers:
- stable interfaces and schemas
- docs that enable others to operate the system
- refactors that reduce complexity and risk

Gold earns (examples):
- reduces onboarding time with clear docs
- removes complexity without breaking behavior
- makes interfaces easier to evolve
