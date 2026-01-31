# ScienceWatch

ScienceWatch fetches RSS/Atom feeds for science journals and arXiv categories.

Goal:
- detect emerging opportunities with evidence

## Run

```bash
./scripts/sciencewatch fetch
```

Outputs:
- `artifacts/sciencewatch/entries.jsonl`
- `artifacts/sciencewatch/snapshots/`
- `artifacts/sciencewatch/state.json`

Configure:
- `tools/sciencewatch/feeds.json`
