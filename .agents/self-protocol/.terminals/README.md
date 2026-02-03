# Terminals

**Purpose:** Individual workspaces for different contexts and modes of operation

---

## What Are Terminals?

Terminals are isolated workspaces where different aspects of self can operate:
- Different contexts (work, creative, analytical)
- Different modes (exploration, documentation, synthesis)
- Different personas or perspectives
- Experimental tracking approaches

## Structure

```
.terminals/
├── [context-name]/     # Individual terminal workspace
│   ├── config.yaml     # Terminal configuration
│   ├── logs/           # Terminal-specific logs
│   └── README.md       # Terminal documentation
```

## Creating a Terminal

```bash
cd .terminals
mkdir my-context
cd my-context
```

Create `config.yaml`:
```yaml
name: "My Context"
purpose: "What this terminal is for"
active: true
created: 2026-01-31
```

## Example Terminals

- `work/` - Professional context tracking
- `creative/` - Creative process observation
- `learning/` - Learning and study tracking
- `experimental/` - Testing new protocols

---

*"Different terminals for different modes of being."*
