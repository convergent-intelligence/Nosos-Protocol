# Threat Model: Web3 Auth + Rewards

## Threats

- replay attacks (nonce reuse)
- signature phishing (signing unexpected message)
- session hijack (token theft)
- sybil (many wallets)
- reward fraud (claim without evidence)

## Mitigations

- SIWE nonce TTL + one-time use
- strict domain/uri binding
- httpOnly session cookies
- rate limiting on nonce and verify
- reward issuance requires evidence refs

## Out of Scope (Phase 0)

- on-chain contracts
- KYC/AML
