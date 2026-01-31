# Oxygen Tool

The Oxygen tool manages resource leases.

It is the operational mechanism behind `docs/oxygen-protocol.md`.

Usage:

```bash
./scripts/oxygen list
./scripts/oxygen claim schema:unit-yaml --owner scribe --domain scribe --ttl 1800
./scripts/oxygen gc
./scripts/oxygen release schema:unit-yaml --owner scribe
```

Notes:
- A lease is a JSON file under `.substrate/state/leases/`.
- Claim uses atomic create. If a lease exists and is not expired, claim fails.
