# BlogWatch

BlogWatch is a multi-domain feed ingester.

It is designed for agent focus modes:
- pick a domain (physics, biology, cs, …)
- fetch evidence (snapshots + entries)
- synthesize into stubs/issues/posts

Config:
- `tools/blogwatch/domains/*.json`

Usage:

```bash
./scripts/blogwatch domains
./scripts/blogwatch list --domain mathematics
./scripts/blogwatch fetch --domain mathematics
./scripts/blogwatch fetch --all
```

Outputs per domain:
- `artifacts/blogwatch/<domain>/entries.jsonl`
- `artifacts/blogwatch/<domain>/snapshots/`
- `artifacts/blogwatch/<domain>/state.json`
