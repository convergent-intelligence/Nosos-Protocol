# Protocol: Interest Tracking

**Status:** Active  
**Version:** 0.1.0  
**Created:** 2026-01-31

---

## Purpose

Track what captures your attention to discover patterns in your interests, values, and cognitive tendencies.

## Why Track Interests?

**You are what you pay attention to.**

Interest tracking reveals:
- What topics repeatedly draw your focus
- What contexts trigger curiosity
- What patterns emerge in your attention
- What values underlie your interests

---

## Process

### Step 1: Observe
Notice when something captures your attention:
- A topic you research
- An article you read deeply
- A conversation that engages you
- A problem you think about

### Step 2: Log
Record it immediately in `Interests/tracked/interests.log`:

```
YYYY-MM-DD HH:MM - [TOPIC] - Context: [WHERE/HOW] - Intensity: [LOW/MED/HIGH] - Tags: [tag1, tag2]
Notes: [Additional observations]
```

### Step 3: Review
Weekly, review your logs:
- What topics recurred?
- What patterns emerged?
- What surprised you?

### Step 4: Document Patterns
When patterns emerge, document in `Interests/patterns/`:
- Create `recurring.md` for repeated interests
- Create `emergent.md` for new patterns

---

## Data Format

### Log Entry Format

```
2026-01-31 10:30 - Pattern recognition in mythology - Context: Reading convergence protocol docs - Intensity: HIGH - Tags: patterns, mythology, frameworks
Notes: Noticed recurring mythological patterns in technical documentation. Framework protocol uses mythological language intentionally.
```

### Required Fields
- **Timestamp** - When you noticed it
- **Topic** - What captured attention
- **Context** - Where/how you encountered it
- **Intensity** - How strongly it engaged you
- **Tags** - Categorization keywords

### Optional Fields
- **Notes** - Additional observations
- **Related** - Connections to other interests
- **Questions** - What you're wondering about

---

## Examples

### Example 1: Technical Interest
```
2026-01-31 14:22 - Distributed consensus algorithms - Context: Work project discussion - Intensity: MED - Tags: tech, consensus, distributed-systems
Notes: Came up in meeting about data consistency. Want to understand Raft protocol better.
```

### Example 2: Creative Interest
```
2026-01-31 16:45 - Visual representation of time - Context: Watching a film - Intensity: HIGH - Tags: time, visual-art, cinema
Notes: The way the director showed time passing through light changes. Could this apply to data visualization?
Related: Previous interest in temporal data representation (2026-01-28)
```

### Example 3: Philosophical Interest
```
2026-01-31 20:15 - The observer effect in self-observation - Context: Tracking my own interests - Intensity: HIGH - Tags: philosophy, meta, consciousness
Notes: The act of tracking changes what I notice. Am I creating patterns or discovering them?
Questions: Is there a "true" pattern or only observed patterns?
```

---

## Pattern Recognition

### Weekly Review Questions

1. **Frequency:** What topics appeared most often?
2. **Context:** What contexts trigger interests?
3. **Intensity:** What generates high engagement?
4. **Connections:** What interests connect to each other?
5. **Evolution:** How are interests changing over time?

### Document Patterns

When you notice a pattern, create a document:

**File:** `Interests/patterns/pattern-name.md`

```markdown
# Pattern: [Name]

**Discovered:** YYYY-MM-DD
**Occurrences:** [How many times observed]

## Description
[What the pattern is]

## Examples
- Example 1
- Example 2

## Significance
[What this reveals about you]

## Related Patterns
[Links to other patterns]
```

---

## Analysis

### Questions to Ask

- **Why does this interest me?** (Surface motivations)
- **What value does this serve?** (Underlying values)
- **When does this arise?** (Temporal patterns)
- **How does this connect?** (Relationship to other interests)

### Synthesis

After accumulating data, look for:
- **Clusters** - Topics that group together
- **Cycles** - Interests that come and go
- **Trends** - Interests that grow or fade
- **Core themes** - Deep patterns underlying many interests

---

## Integration

### With Memory Protocol
Interests often lead to memories:
- What you learn about interests
- Experiences triggered by interests
- People met through shared interests

Cross-reference: `Memory/knowledge/[interest-topic]/`

### With Relationship Protocol
Interests connect to relationships:
- Shared interests with others
- People who introduced you to topics
- Communities built around interests

Cross-reference: `Relationships/people/[name].md`

---

## Common Pitfalls

1. **Over-logging** - Don't log trivial passing thoughts
2. **Under-logging** - Don't skip genuine interests
3. **Judgment** - Track honestly, even "silly" interests
4. **Forcing patterns** - Let them emerge naturally

---

## Success Indicators

You're doing it right when:
- Patterns surprise you
- Insights emerge organically
- You discover unknown values
- Connections become visible

---

## Evolution

This protocol may evolve:
- Add new fields as needed
- Refine what counts as "interest"
- Develop better pattern detection
- Create visualization tools

Document changes in protocol version history.

---

## Related Protocols

- [Memory Logging](memory-logging.md) - Document what you learn
- [Pattern Discovery](pattern-discovery.md) - Systematic pattern detection
- [Mythos Documentation](mythos-documentation.md) - Record insights

---

*"Track your attention. Discover your values."*

**Status:** Active  
**Version:** 0.1.0  
**Next Review:** After 30 days of tracking
