# Signal Tool

Creates structured signals as files under `.bridges/signals/`.

Signals are coordination artifacts:
- proclamation: broadcast, no response expected
- missive: direct request, response may be expected
- council_call: decision request (votes/ack)

## Usage

From the scaffold root:

```bash
./scripts/signal proclamation --topic "status" --claim "Phase 0 scaffold ready" --from scribe --to all
./scripts/signal missive --topic "secrets" --claim "Need quarantine policy" --from guardian --to watcher --expects-response
./scripts/signal council_call --topic "schema" --claim "Freeze unit.yaml v0.1" --from scribe --to council --expects-response --response-by 2026-02-01T00:00:00Z
```
