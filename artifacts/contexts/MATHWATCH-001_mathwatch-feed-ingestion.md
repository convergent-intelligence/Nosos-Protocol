# Context Capsule: MathWatch feed ingestion

Work ID: MATHWATCH-001
Kind: plan
Domain: scribe
Priority: medium
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:33:05Z

## Objective

Fetch math feeds into artifacts/mathwatch for opportunity scanning

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
- `docs/math/mathwatch.md`
- `scripts/mathwatch`
- `tools/mathwatch/feeds.json`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-052924_proclamation_plan.json`
- `.bridges/signals/20260130-052559_proclamation_plan.json`
- `.bridges/signals/20260130-051335_proclamation_plan.json`
- `.bridges/signals/20260130-051335_missive_assignment.json`
- `.bridges/signals/20260130-051043_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/math/mathwatch.md`

```
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
```

### `scripts/mathwatch`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/mathwatch/mathwatch.py" "$@"
```

### `tools/mathwatch/feeds.json`

```
{
  "version": "0.1",
  "feeds": [
    {
      "id": "tao",
      "name": "Terry Tao",
      "url": "https://terrytao.wordpress.com/feed/",
      "tags": ["analysis", "additive", "exposition"]
    },
    {
      "id": "gowers",
      "name": "Gowers",
      "url": "https://gowers.wordpress.com/feed/",
      "tags": ["combinatorics", "exposition"]
    },
    {
      "id": "kalai",
      "name": "Gil Kalai",
      "url": "https://gilkalai.wordpress.com/feed/",
      "tags": ["combinatorics", "complexity", "quantum"]
    },
    {
      "id": "quanta",
      "name": "Quanta Magazine",
      "url": "https://www.quantamagazine.org/feed/",
      "tags": ["math", "science", "exposition"]
    },
    {
      "id": "mathoverflow",
      "name": "MathOverflow",
      "url": "https://mathoverflow.net/feeds",
      "tags": ["problems", "research"]
    },
    {
      "id": "arxiv_math",
      "name": "arXiv math (all)",
      "url": "https://arxiv.org/rss/math",
      "tags": ["arxiv", "preprints"]
    },
    {
      "id": "arxiv_cs_cc",
      "name": "arXiv cs.CC",
      "url": "https://arxiv.org/rss/cs.CC",
      "tags": ["complexity", "theory", "preprints"]
    }
  ]
}
```

