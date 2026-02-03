# Bridges

**Purpose:** Connect Self-Protocol to external systems and other protocols

---

## What Are Bridges?

Bridges are connection points that allow Self-Protocol to:
- Integrate with other protocols (Convergence, Voice, etc.)
- Connect to external systems and APIs
- Share data across boundaries
- Establish communication protocols

## Structure

```
.bridges/
├── convergence/        # Links to Convergence Protocol
├── voice/              # Links to Voice Protocol
├── external/           # External system connections
└── protocols/          # Communication protocol definitions
```

## Bridge Types

### Protocol Bridges (`convergence/`, `voice/`)
Connect to other protocols in the ecosystem
- Shared data formats
- Cross-protocol insights
- Unified mythos documentation

### External Bridges (`external/`)
Connect to external systems
- APIs and services
- Data import/export
- Third-party integrations

### Communication Bridges (`protocols/`)
Define how data flows between systems
- Message formats
- Handshake protocols
- Data synchronization

## Creating a New Bridge

1. Create directory: `.bridges/[bridge-name]/`
2. Define protocol: `[bridge-name]/protocol.md`
3. Implement connection: `[bridge-name]/connector.py`
4. Document: `[bridge-name]/README.md`

---

*"Bridges connect islands of understanding."*
