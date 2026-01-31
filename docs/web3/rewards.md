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
