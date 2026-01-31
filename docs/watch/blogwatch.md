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
