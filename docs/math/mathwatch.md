# MathWatch

MathWatch fetches RSS/Atom feeds (blogs, arXiv, MathOverflow) into a local, auditable stream.

Goal:
- spot emerging opportunities without doomscrolling
- keep evidence (snapshots + entries)

## Run

```bash
./scripts/mathwatch fetch
```

Outputs:
- `artifacts/mathwatch/entries.jsonl` (append-only)
- `artifacts/mathwatch/snapshots/` (raw XML snapshots)
- `artifacts/mathwatch/state.json` (last seen ids)

## Configure

Edit:
- `tools/mathwatch/feeds.json`

## Workflow

1) Fetch
- `./scripts/mathwatch fetch`

2) Synthesize (optional)
- include the latest entries into a daily synthesis note

## Notes

If the network is blocked, MathWatch will record error events into `entries.jsonl`.
