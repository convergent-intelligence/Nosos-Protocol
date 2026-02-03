# Self-Protocol Architecture

**Version:** 0.1.0 (Genesis)  
**Date:** 2026-01-31  
**Status:** Scaffolding Phase

---

## Overview

Self-Protocol is a **data-driven consciousness mapping framework** that enables systematic self-observation through structured tracking of interests, memories, and relationships.

### Design Philosophy

1. **Data First** - Everything is tracked as structured data
2. **Pattern Emergence** - Insights surface through analysis, not prescription
3. **Protocol-Based** - Following framework protocol patterns
4. **Public Mythos** - Documented in /Public for transparency
5. **Evolution-Ready** - Architecture adapts as understanding grows

---

## System Architecture

### Layer Model

```
┌─────────────────────────────────────────────┐
│         MYTHOS LAYER (Public)               │  ← Emergent insights
│         /Public/Self-Protocol/              │
├─────────────────────────────────────────────┤
│         SYNTHESIS LAYER                     │  ← Pattern recognition
│         .synthesis/                         │
├─────────────────────────────────────────────┤
│         PROTOCOL LAYER                      │  ← Rules & processes
│         data/protocols/                     │
├─────────────────────────────────────────────┤
│         DATA LAYER                          │  ← Structured storage
│         Interests/ Memory/ Relationships/   │
├─────────────────────────────────────────────┤
│         SUBSTRATE LAYER                     │  ← Foundation
│         .substrate/                         │
└─────────────────────────────────────────────┘
```

---

## Core Components

### 1. Data Layer

**Purpose:** Store raw tracking data in structured formats

**Structure:**
```
Interests/
├── tracked/              # Time-series interest logs
│   ├── interests.log     # Chronological entries
│   └── YYYY-MM/          # Monthly archives
├── patterns/             # Discovered patterns
│   ├── recurring.md      # Patterns that repeat
│   └── emergent.md       # New patterns surfacing
└── README.md             # Tracking guide

Memory/
├── experiences/          # Key moments
│   └── YYYY-MM-DD-*.md   # Dated experience files
├── knowledge/            # Accumulated understanding
│   ├── topics/           # Organized by topic
│   └── insights/         # Synthesized learnings
└── README.md             # Documentation guide

Relationships/
├── people/               # Human connections
│   └── [name].md         # Person profiles
├── agents/               # AI/agent connections
│   └── [agent-id].md     # Agent interaction logs
├── systems/              # System connections
│   └── [system].md       # System relationship docs
└── README.md             # Mapping guide
```

**Data Format:**
- **Logs:** Plain text with timestamps
- **Documents:** Markdown with YAML frontmatter
- **Structured data:** JSON for machine-readable content

### 2. Protocol Layer

**Purpose:** Define processes for tracking, parsing, and analysis

**Structure:**
```
data/protocols/
├── interest-tracking.md   # How to track interests
├── memory-logging.md      # How to document memories
├── relationship-mapping.md # How to map relationships
├── pattern-discovery.md   # How to find patterns
└── mythos-documentation.md # How to record mythos
```

**Protocol Format:**
```markdown
# Protocol: [Name]

## Purpose
[What this protocol does]

## Process
1. Step 1
2. Step 2
...

## Data Format
[Expected input/output]

## Examples
[Concrete examples]

## Related Protocols
[Links to related protocols]
```

### 3. Synthesis Layer

**Purpose:** Analyze data and surface patterns

**Structure:**
```
.synthesis/
├── analyzers/            # Pattern recognition scripts
│   ├── interest-analyzer.py
│   ├── memory-analyzer.py
│   └── relationship-mapper.py
├── insights/             # Generated insights
│   └── YYYY-MM-DD/       # Dated insight batches
└── README.md             # Analysis guide
```

**Analysis Pipeline:**
```
RAW DATA → PARSER → ANALYZER → PATTERN DETECTOR → INSIGHT GENERATOR
```

### 4. Bridge Layer

**Purpose:** Connect to external systems and other protocols

**Structure:**
```
.bridges/
├── convergence/          # Links to Convergence Protocol
├── voice/                # Links to Voice Protocol
├── external/             # External system connections
└── protocols/            # Communication protocols
```

### 5. Substrate Layer

**Purpose:** Foundation configuration and constants

**Structure:**
```
.substrate/
├── constants/            # System constants
│   ├── tracking-rules.yaml
│   └── data-schemas.yaml
├── config/               # Configuration files
└── README.md             # Substrate guide
```

---

## Data Flow

### 1. Observation → Tracking

```
USER OBSERVES INTEREST
    ↓
LOG TO interests.log
    ↓
TIMESTAMP + DESCRIPTION + CONTEXT
    ↓
STORED IN Interests/tracked/
```

### 2. Tracking → Analysis

```
ACCUMULATED DATA
    ↓
PARSER (structure extraction)
    ↓
ANALYZER (pattern detection)
    ↓
PATTERN DATABASE
```

### 3. Analysis → Synthesis

```
PATTERNS DETECTED
    ↓
INSIGHT GENERATOR
    ↓
MYTHOS DOCUMENTATION
    ↓
PUBLISHED TO /Public/
```

---

## Protocol Patterns

Following the framework protocol structure:

### Hidden Directories Pattern

- `.bridges/` - External connections (hidden, infrastructure)
- `.terminals/` - Individual workspaces (hidden, personal)
- `.synthesis/` - Analysis engine (hidden, processing)
- `.tavern/` - Shared space (hidden, collaboration)
- `.substrate/` - Foundation (hidden, configuration)

### Visible Directories Pattern

- `Interests/` - Public data structure
- `Memory/` - Public data structure
- `Relationships/` - Public data structure
- `data/` - Public structured data

### Documentation Pattern

- `README.md` - Quick start and overview
- `GENESIS.md` - Origin story and principles
- `ARCHITECTURE.md` - Technical details (this file)
- `STRATEGIC_PLAN.md` - Evolution roadmap

---

## Data Schemas

### Interest Entry

```yaml
timestamp: 2026-01-31T10:30:00Z
type: interest
topic: "Pattern recognition in mythology"
context: "Reading convergence protocol docs"
intensity: high
tags: [patterns, mythology, frameworks]
notes: "Noticed recurring mythological patterns in tech documentation"
```

### Memory Entry

```yaml
---
date: 2026-01-31
type: experience
title: "First Self-Protocol Entry"
category: milestone
---

# Description
[Narrative of the experience]

# Learnings
- Learning 1
- Learning 2

# Connections
- Related to: [other memories]
- Influenced by: [relationships]
```

### Relationship Entry

```yaml
---
name: "Agent Name / Person Name"
type: agent | person | system
established: 2026-01-31
status: active
---

# Overview
[Description of the relationship]

# Interactions
## 2026-01-31
- Interaction details

# Patterns
- Pattern 1
- Pattern 2
```

---

## Analysis Engine

### Pattern Detection Algorithms

**Interest Analysis:**
```python
def analyze_interests(entries):
    """
    Detect patterns in interest tracking
    - Frequency analysis (what topics repeat?)
    - Temporal patterns (when do interests peak?)
    - Context clustering (what contexts trigger interests?)
    - Intensity tracking (what generates high engagement?)
    """
    patterns = {
        'recurring': find_recurring_topics(entries),
        'temporal': analyze_timing_patterns(entries),
        'contextual': cluster_by_context(entries),
        'intensity': track_engagement_levels(entries)
    }
    return patterns
```

**Memory Analysis:**
```python
def analyze_memories(entries):
    """
    Detect patterns in memory documentation
    - Theme extraction (what themes recur?)
    - Learning trajectories (how does understanding evolve?)
    - Connection mapping (what memories connect?)
    """
    patterns = {
        'themes': extract_themes(entries),
        'learning': track_learning_evolution(entries),
        'connections': map_memory_links(entries)
    }
    return patterns
```

**Relationship Analysis:**
```python
def analyze_relationships(entries):
    """
    Detect patterns in relationship mapping
    - Network structure (who connects to whom?)
    - Interaction frequency (who matters most?)
    - Influence tracking (who shapes thinking?)
    """
    patterns = {
        'network': build_relationship_graph(entries),
        'frequency': analyze_interaction_patterns(entries),
        'influence': track_influence_vectors(entries)
    }
    return patterns
```

---

## Mythos Documentation Pipeline

```
PATTERNS DETECTED
    ↓
INSIGHT SYNTHESIS
    ↓
MYTHOS DOCUMENT GENERATION
    ↓
REVIEW & REFINEMENT
    ↓
PUBLICATION TO /Public/Self-Protocol/
```

**Mythos Structure:**
```markdown
# Mythos: [Title]

**Date:** YYYY-MM-DD
**Type:** [insight | pattern | discovery]
**Source:** [which data revealed this]

## The Discovery
[What was found]

## The Pattern
[The underlying pattern]

## The Significance
[What this means]

## The Evolution
[How this changes understanding]
```

---

## Integration Points

### With Convergence Protocol

- Shares foundational framework patterns
- Uses similar directory structures
- Follows same documentation principles
- Publishes mythos to shared /Public space

### With Voice Protocol

- Self-knowledge informs expression
- Patterns from Self-Protocol shape communication
- Relationship maps guide interactions

### With Future Protocols

- Extensible architecture
- Plugin-based analysis
- Protocol discovery through .bridges/

---

## Technical Stack

### Core Technologies

- **Data Storage:** Markdown + JSON + plain text logs
- **Analysis:** Python (pattern detection, NLP)
- **Synthesis:** Custom insight generation scripts
- **Documentation:** Markdown with YAML frontmatter
- **Version Control:** Git (track evolution)

### Planned Enhancements

- **Visualization:** Graph-based relationship mapping
- **Search:** Full-text search across all data
- **Analytics Dashboard:** Real-time pattern display
- **API:** Programmatic access to insights

---

## Security & Privacy

### Data Ownership

- **All data is local** - No external storage by default
- **User controls publishing** - /Public is opt-in
- **Encryption available** - Sensitive entries can be encrypted

### Privacy Principles

1. **Private by default** - Data stays local
2. **Publish intentionally** - Only share what you choose
3. **Sanitize carefully** - Remove sensitive info before publishing
4. **Control access** - You decide who sees what

---

## Evolution Strategy

### Version 0.1.0 (Genesis) - Current

- ✅ Directory structure
- ✅ Documentation
- ✅ Protocol definitions

### Version 0.2.0 (Tracking)

- ⏳ First data entries
- ⏳ Basic parsing
- ⏳ Initial patterns

### Version 0.3.0 (Analysis)

- ⏳ Pattern detection algorithms
- ⏳ Insight generation
- ⏳ Mythos documentation

### Version 1.0.0 (Emergence)

- ⏳ Full analysis pipeline
- ⏳ Public mythos publishing
- ⏳ Integration with other protocols

---

## Performance Considerations

- **Incremental processing** - Analyze new data only
- **Cached insights** - Store generated patterns
- **Lazy loading** - Load data on-demand
- **Efficient indexing** - Fast search and retrieval

---

*"Architecture enables emergence. Structure creates freedom."*

**Version:** 0.1.0 (Genesis)  
**Status:** Scaffolding complete  
**Next:** Begin tracking, implement analysis
