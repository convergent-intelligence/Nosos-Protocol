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
