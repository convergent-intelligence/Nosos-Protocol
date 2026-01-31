# Runbook (Draft)

## Local Setup

- Prereqs:
- Install:
- Run:
- Test:

## Operations

- Health check:
- Run `./scripts/health.sh` to produce a JSON health snapshot and update `.substrate/state/health.json`.
- Logs:
- Metrics:
- Common failures:

## Deploy

- Environments:
- Rollback:
- Migrations:

## Backups

- Default backup (no blobs): `./scripts/backup.sh`
- Full backup (includes blobs): `./scripts/backup.sh --with-blobs`

Notes:
- the blob store can be large; keep backups intentional
- the distro build excludes user data; backups do not

## Restore

- Restore a backup tarball into an empty directory:

```bash
./scripts/restore.sh backups/asf-backup-YYYYMMDD-HHMMSS.tar.gz /tmp/asf-restore
```
