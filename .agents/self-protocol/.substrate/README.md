# Substrate

**Purpose:** The foundation layer - constants, configurations, and core rules

---

## What Is The Substrate?

The substrate is the unchanging foundation upon which everything else is built:
- System constants and rules
- Configuration files
- Data schemas
- Core principles

## Structure

```
.substrate/
├── constants/          # System constants
│   ├── tracking-rules.yaml
│   ├── data-schemas.yaml
│   └── system-limits.yaml
├── config/             # Configuration files
│   ├── analysis-config.yaml
│   └── export-config.yaml
└── README.md           # This file
```

## Constants vs Configuration

### Constants (`constants/`)
**Fixed rules that rarely change:**
- Data format schemas
- System boundaries
- Core principles

### Configuration (`config/`)
**Settings that can be adjusted:**
- Analysis parameters
- Export preferences
- Integration settings

## Example: Tracking Rules

```yaml
# constants/tracking-rules.yaml

interest_tracking:
  min_entry_length: 10
  required_fields: [timestamp, topic, context]
  optional_fields: [intensity, tags, notes]
  
memory_documentation:
  required_frontmatter: [date, type, title]
  supported_types: [experience, knowledge, insight]
  
relationship_mapping:
  entity_types: [person, agent, system]
  required_fields: [name, type, established]
```

## Example: Data Schemas

```yaml
# constants/data-schemas.yaml

interest_entry:
  timestamp: datetime
  topic: string
  context: string
  intensity: enum [low, medium, high]
  tags: list[string]
  notes: string

memory_entry:
  date: date
  type: enum [experience, knowledge, insight]
  title: string
  category: string
  content: markdown
  
relationship_entry:
  name: string
  type: enum [person, agent, system]
  established: date
  status: enum [active, dormant, archived]
```

---

*"The substrate is the bedrock. Everything builds upon it."*
