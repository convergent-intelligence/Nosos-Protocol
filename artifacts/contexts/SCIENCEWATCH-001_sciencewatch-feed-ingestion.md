# Context Capsule: ScienceWatch feed ingestion

Work ID: SCIENCEWATCH-001
Kind: plan
Domain: scribe
Priority: medium
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:36:04Z

## Objective

Fetch science feeds into artifacts/sciencewatch for opportunity scanning

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
- `docs/science/sciencewatch.md`
- `scripts/sciencewatch`
- `tools/sciencewatch/feeds.json`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-053305_proclamation_plan.json`
- `.bridges/signals/20260130-052924_proclamation_plan.json`
- `.bridges/signals/20260130-052559_proclamation_plan.json`
- `.bridges/signals/20260130-051335_proclamation_plan.json`
- `.bridges/signals/20260130-051335_missive_assignment.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/science/sciencewatch.md`

```
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
```

### `scripts/sciencewatch`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/sciencewatch/sciencewatch.py" "$@"
```

### `tools/sciencewatch/feeds.json`

```
{
  "version": "0.1",
  "feeds": [
    {
      "id": "nature",
      "name": "Nature",
      "url": "https://www.nature.com/nature.rss",
      "tags": ["science", "journal"]
    },
    {
      "id": "science",
      "name": "Science",
      "url": "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science",
      "tags": ["science", "journal"]
    },
    {
      "id": "pnas",
      "name": "PNAS",
      "url": "https://www.pnas.org/action/showFeed?type=etoc&feed=rss&jc=pnas",
      "tags": ["science", "journal"]
    },
    {
      "id": "arxiv_physics",
      "name": "arXiv physics (all)",
      "url": "https://arxiv.org/rss/physics",
      "tags": ["physics", "preprints"]
    },
    {
      "id": "arxiv_quant_ph",
      "name": "arXiv quant-ph",
      "url": "https://arxiv.org/rss/quant-ph",
      "tags": ["quantum", "physics", "preprints"]
    },
    {
      "id": "arxiv_q_bio",
      "name": "arXiv q-bio",
      "url": "https://arxiv.org/rss/q-bio",
      "tags": ["biology", "preprints"]
    },
    {
      "id": "arxiv_stat_ml",
      "name": "arXiv stat.ML",
      "url": "https://arxiv.org/rss/stat.ML",
      "tags": ["ml", "stats", "preprints"]
    }
  ]
}
```

