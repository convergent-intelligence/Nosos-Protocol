# Focus Ritual

Focus is the shortcut pattern:
- capture the current state in one bounded snapshot
- translate state into the next safe action

Command:

```bash
./scripts/focus
./scripts/focus route
```

Select a mode (level):

```bash
./scripts/focus status --level 2
./scripts/focus route --level 3
```

It writes:
- `.substrate/state/focus.json`

It includes:
- health, field Z, budgets, active/next items

Modes:
- Focus levels are a mode of operation (weights), not a feature.
- See `docs/ops/focus-modes.md`.

The goal is intelligent forgetting:
- once a level is encoded in tooling, you don't need to remember the steps
