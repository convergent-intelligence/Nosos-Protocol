# GitHubWatch

GitHubWatch tracks curated GitHub repositories via public Atom feeds:
- releases
- issues
- pull requests
- commits

This is for keeping ahead of CS evolution without relying on external platforms as a primary domain.

## Domains

```bash
./scripts/githubwatch domains
./scripts/githubwatch list --domain computer_science
```

## Fetch

```bash
./scripts/githubwatch fetch --domain computer_science
```

Outputs:
- `artifacts/githubwatch/<domain>/entries.jsonl`
- `artifacts/githubwatch/<domain>/snapshots/`
