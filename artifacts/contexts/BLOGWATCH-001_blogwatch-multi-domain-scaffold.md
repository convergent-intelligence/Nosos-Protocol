# Context Capsule: BlogWatch multi-domain scaffold

Work ID: BLOGWATCH-001
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:44:16Z

## Objective

Unified blogwatch across major fields with team-based categorization and evidence artifacts

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
- `docs/watch/blogwatch.md`
- `scripts/blogwatch`
- `tools/blogwatch/domains/general_science.json`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-053604_proclamation_plan.json`
- `.bridges/signals/20260130-053305_proclamation_plan.json`
- `.bridges/signals/20260130-052924_proclamation_plan.json`
- `.bridges/signals/20260130-052559_proclamation_plan.json`
- `.bridges/signals/20260130-051335_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/watch/blogwatch.md`

```
# BlogWatch

BlogWatch is the unified feed ingester for major domains.

The point is focus:
- agents choose a domain
- ingest evidence locally
- synthesize into opportunities (stubs/issues/posts)

## Domains

```bash
./scripts/blogwatch domains
```

## Fetch

```bash
./scripts/blogwatch fetch --domain physics
./scripts/blogwatch fetch --all
```

Outputs:
- `artifacts/blogwatch/<domain>/entries.jsonl`
- `artifacts/blogwatch/<domain>/snapshots/`
- `artifacts/blogwatch/<domain>/state.json`

## Configure

Each domain has a JSON file with teams and feeds:
- `tools/blogwatch/domains/`

Teams are how we organize bloggers and sources inside a domain.
```

### `scripts/blogwatch`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ASF_ROOT="${root_dir}"

exec python3 "${root_dir}/tools/blogwatch/blogwatch.py" "$@"
```

### `tools/blogwatch/domains/general_science.json`

```
{
  "version": "0.1",
  "domain": "general_science",
  "name": "General Science",
  "description": "Broad science sources that are cross-domain.",
  "teams": [
    {
      "id": "journals",
      "name": "Journals",
      "feeds": [
        {"id": "nature", "name": "Nature", "url": "https://www.nature.com/nature.rss", "tags": ["journal"]},
        {"id": "science", "name": "Science", "url": "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science", "tags": ["journal"]},
        {"id": "pnas", "name": "PNAS", "url": "https://www.pnas.org/action/showFeed?type=etoc&feed=rss&jc=pnas", "tags": ["journal"]}
      ]
    },
    {
      "id": "magazines",
      "name": "Magazines",
      "feeds": [
        {"id": "quanta", "name": "Quanta", "url": "https://www.quantamagazine.org/feed/", "tags": ["exposition"]}
      ]
    }
  ]
}
```

