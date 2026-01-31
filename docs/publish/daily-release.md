# Daily Release: 1 Post Per Day

Goal: one evidence-first post per day in a chosen knowledge domain.

Boundaries:
- `docs/publish/policy.md`

Principles:
- we do not publish vibes
- every post links to artifacts and commands that reproduce the claim

## Create Today’s Draft

Pick a domain from BlogWatch:

```bash
./scripts/blogwatch domains
```

Create the draft (and fetch sources):

```bash
./scripts/daily --domain mathematics
```

Web3 note:
- publishing should require an authenticated wallet session once the app exists

Draft path:
- `sites/convergent-intelligence/drafts/YYYY-MM-DD_<domain>.md`

## Publish (Local)

Publishing moves the draft into date-based posts and updates an index:

```bash
./scripts/publish sites/convergent-intelligence/drafts/YYYY-MM-DD_mathematics.md
```

## Evidence

Source ingestion artifacts live under:
- `artifacts/blogwatch/<domain>/`

Daily creation record lives under:
- `artifacts/publish/daily/`
