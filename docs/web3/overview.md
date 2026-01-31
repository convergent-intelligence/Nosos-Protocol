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
