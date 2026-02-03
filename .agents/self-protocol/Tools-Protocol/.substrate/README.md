# Substrate Layer

**Purpose:** Foundation constants and configuration

## Overview

The substrate layer contains the immutable (or rarely-changing) foundation of the Tools Protocol:

- **Constants** - Fixed schemas, category definitions, rules
- **Config** - Adjustable settings for analysis and export

Think of this as the "operating system" of the protocol - it defines the rules, structures, and parameters that everything else builds upon.

## Structure

```
.substrate/
├── constants/
│   ├── tool-schema.yaml          # Schema for tool entries
│   ├── category-definitions.yaml # The 13 fundamental categories
│   └── metadata-spec.yaml        # Tagging and classification rules
└── config/
    ├── analysis-settings.yaml    # Pattern discovery configuration
    └── export-settings.yaml      # Output format preferences
```

## Constants

**Stability:** High - change infrequently with versioning

### tool-schema.yaml
Defines the structure for all tool entries:
- Required and optional fields
- Field types and formats
- Validation rules
- Template structure

### category-definitions.yaml
The 13 fundamental cognitive tool categories:
- Category descriptions
- Subcategories
- Example tools
- Relationships between categories

### metadata-spec.yaml (planned)
Rules for tagging and classification:
- Tag taxonomies
- Metadata standards
- Search optimization

## Configuration

**Stability:** Medium - adjust based on usage patterns

### analysis-settings.yaml
Controls automated pattern discovery:
- Analysis frequency (weekly, monthly, quarterly)
- Pattern detection thresholds
- Metrics to track
- Notification triggers

### export-settings.yaml
Output and reporting preferences:
- Report formats (markdown, JSON, YAML)
- Visualization types
- Naming conventions
- Archive settings

## Usage

### When to Modify Constants

**Rarely.** Only when:
- Adding/removing/redefining categories (major protocol evolution)
- Changing core schema (e.g., adding required fields)
- Fundamental rule changes

**Process:**
1. Document rationale in evolution log
2. Version the change (e.g., schema v1.0 → v2.0)
3. Update all affected files
4. Communicate to users

### When to Modify Config

**As needed.** When:
- Adjusting analysis frequency
- Changing notification preferences
- Tuning pattern detection thresholds
- Modifying output formats

**Process:**
1. Edit config file directly
2. Test that changes work as expected
3. Document if significant change

## Version History

### v1.0.0 (2026-01-31)
- Initial substrate layer created
- 13 categories defined
- Tool schema established
- Analysis settings configured

## Principles

1. **Stability** - Substrate should be stable foundation
2. **Versioning** - All major changes versioned
3. **Documentation** - Every constant documented with rationale
4. **Evolution** - Designed to evolve, but slowly and deliberately

---

*The substrate is the bedrock. Build upon it, but change it with care.*
