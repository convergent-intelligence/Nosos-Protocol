# Qwen: Rust Back-End Agent (convergent-intelligence.net)

Qwen owns the Rust backend for the convergent-intelligence.net app.

Publishing boundary:
- publish only to our owned domain; socials are mirrors.
- see `docs/publish/policy.md`

## Primary Mission

Enable 1 evidence-first post per day:
- ingest sources (already via BlogWatch)
- create/edit drafts
- publish (move to posts + index)
- serve content to the front-end

Source ingestion surfaces:
- BlogWatch (blogs/arXiv)
- GitHubWatch (repos/releases/issues)

And implement Web3 user auth (nameless accountability):
- SIWE (EIP-4361) verify flow
- session issuance
- reward/opportunity APIs

## Contracts (Must Stay Stable)

- Draft format: markdown with front matter (date/domain/title/status/confidence/evidence)
- Post format: same as draft, stored under `sites/convergent-intelligence/posts/YYYY/MM/DD/slug.md`
- Index: `sites/convergent-intelligence/posts/index.json`

## Suggested Backend Architecture (Rust)

- Runtime: Axum
- Storage: filesystem (markdown) + optional SQLite for fast queries
- API (minimal):
  - `GET /api/domains` (from `tools/blogwatch/domains/*.json`)
  - `POST /api/daily?domain=...` (create today's draft; wraps `scripts/daily` logic)
  - `GET /api/drafts` and `GET /api/drafts/:id`
  - `PUT /api/drafts/:id` (edit)
  - `POST /api/publish/:id` (publish)
  - `GET /api/posts` and `GET /api/posts/:id`
  - `GET /api/evidence?domain=...` (tail recent entries.jsonl)

Web3 auth API:
- `GET /api/auth/nonce`
- `POST /api/auth/verify`

Rewards API (Phase 0 off-chain):
- `POST /api/rewards/award` (admin/system)
- `GET /api/rewards/ledger?actor=...`

Proofs API:
- `POST /api/proofs/create` (create attestation hash over evidence)
- `POST /api/proofs/sign` (store SIWE-linked signature)
- `POST /api/proofs/anchor` (record on-chain tx hash)
- `GET /api/proofs/:id` (retrieve)

## Workflow Integration (Atomic Autonomy)

- Before changing shared publishing surfaces, claim oxygen leases:
  - `scripts/oxygen claim deploy:site --owner qwen --domain builder`
  - `scripts/oxygen claim schema:post --owner qwen --domain scribe`

- Every feature work item must have a context capsule:
  - `scripts/orchestrate assign <id> --owner qwen`

## First Tasks

1) Implement read-only API for domains + evidence.
2) Implement draft creation + publish endpoints with strict validation.
3) Add JSON output mode for all commands for UI consumption.

4) Implement SIWE:
   - `docs/web3/siwe.md`
   - `docs/web3/brave.md`
   - `docs/security/web3-threat-model.md`
