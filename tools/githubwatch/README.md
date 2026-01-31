# GitHubWatch

GitHubWatch ingests GitHub repository Atom feeds without requiring auth.

It is designed for agent focus:
- pick a domain (e.g. computer_science)
- fetch updates across curated repos
- keep evidence (raw snapshots + append-only entries)

Usage:

```bash
./scripts/githubwatch domains
./scripts/githubwatch list --domain computer_science
./scripts/githubwatch fetch --domain computer_science
```

Outputs:
- `artifacts/githubwatch/<domain>/entries.jsonl`
- `artifacts/githubwatch/<domain>/snapshots/`
- `artifacts/githubwatch/<domain>/state.json`
