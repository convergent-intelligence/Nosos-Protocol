# Context Capsule: Web3 user system scaffold

Work ID: WEB3-001
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:53:16Z

## Objective

Wallet-based pseudonymous auth + rewards/opportunities + Brave integration

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
- `docs/web3/overview.md`
- `docs/web3/siwe.md`
- `docs/web3/brave.md`
- `docs/web3/rewards.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-054927_proclamation_plan.json`
- `.bridges/signals/20260130-054416_proclamation_plan.json`
- `.bridges/signals/20260130-053604_proclamation_plan.json`
- `.bridges/signals/20260130-053305_proclamation_plan.json`
- `.bridges/signals/20260130-052924_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/web3/overview.md`

```
# Web3 User System (Nameless Accountability)

Goal: a user system that is pseudonymous, wallet-based, and auditable.

Principles:
- no email/password
- identity = wallet ownership proven by signature
- accountability = signed actions + append-only event log
- rewards/opportunities are first-class surfaces

Recommended default (EVM/Brave):
- EIP-1193 provider (`window.ethereum`)
- SIWE (EIP-4361) for authentication

## Core Objects

- Identity
  - `did:pkh` style identifier (e.g. `did:pkh:eip155:1:0x...`)
  - wallet address (public)

- Session
  - short-lived server session or JWT
  - issued only after SIWE verify

- Reward
  - off-chain points ledger (append-only) as the default
  - optional future: on-chain token/badge minting

- Opportunity
  - a claimable work item (bounty, task, research prompt)
  - must link evidence and measurement

## High-Level Flow

1) Connect wallet (Brave wallet or any EIP-1193)
2) Request nonce from backend
3) Sign SIWE message
4) Backend verifies signature and issues session
5) User can draft/publish and earn rewards

## Why This Fits Atomic Autonomy

- identity is explicit and verifiable
- actions are logged
- no central credential store
```

### `docs/web3/siwe.md`

```
# SIWE (EIP-4361) Authentication

## Endpoints (Rust backend)

- `GET /api/auth/nonce`
  - returns `{ nonce }`

- `POST /api/auth/verify`
  - input: `{ message, signature }`
  - verifies:
    - nonce matches and not reused
    - signature recovers address
    - domain and uri match expected origin
    - chainId allowed
  - output: session cookie or JWT

## Replay Protection

- store used nonces (TTL)
- bind nonce to an origin (domain)

## Session Model

Default:
- httpOnly cookie session
- short TTL + refresh

Alternative:
- JWT
```

### `docs/web3/brave.md`

```
# Brave Browser Integration

Brave Wallet typically exposes an EIP-1193 provider:
- `window.ethereum`

Frontend expectations (Gems):
- detect provider
- request accounts
- build SIWE message
- sign via `personal_sign` / `eth_signTypedData_v4` depending on SIWE lib

Backend expectations (Qwen):
- verify EIP-191 signature (SIWE)
- map recovered address to identity id

Do not assume Brave-only.
Treat Brave as a first-class target, but keep EIP-1193 compatible.
```

### `docs/web3/rewards.md`

```
# Rewards + Opportunities (Web3)

Default (Phase 0): off-chain rewards, on-chain optional later.

## Reward Ledger (Off-chain)

- append-only events
- deterministic point calculation
- verifiable linkage to actions (publish, review, solve)

Storage:
- `artifacts/rewards/ledger.jsonl`

Event schema:

```json
{
  "ts": "...",
  "actor": "did:pkh:eip155:1:0x...",
  "action": "publish_post",
  "ref": "sites/convergent-intelligence/posts/...",
  "points": 10,
  "evidence": ["artifacts/..."],
  "notes": "..."
}
```

## On-chain (Later)

Optional future path:
- mint badges (ERC-721) or points token (ERC-20)
- keep the off-chain ledger as the source-of-truth for intent and audit

## Opportunities

Opportunity is a work item with reward attached.

It must include:
- objective
- measurement
- evidence requirements
- payout rule
```

