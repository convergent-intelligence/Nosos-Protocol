# Interests

**Track what captures your attention to discover your values**

---

## Purpose

This directory contains:
- **tracked/** - Raw interest logs (chronological tracking)
- **patterns/** - Discovered patterns in interests

## Quick Start

### Log an Interest

```bash
cd tracked/
echo "$(date +%Y-%m-%d\ %H:%M) - [TOPIC] - Context: [CONTEXT] - Intensity: [LOW/MED/HIGH] - Tags: [tags]" >> interests.log
echo "Notes: [Your observations]" >> interests.log
echo "" >> interests.log
```

### Example Entry

```
2026-01-31 14:30 - Pattern recognition in mythology - Context: Reading convergence docs - Intensity: HIGH - Tags: patterns, mythology, frameworks
Notes: Noticed how technical docs use mythological language intentionally. Framework protocol patterns.

```

---

## Structure

```
Interests/
├── README.md              # This file
├── tracked/               # Chronological logs
│   ├── interests.log      # Main tracking file
│   └── YYYY-MM/           # Monthly archives
└── patterns/              # Discovered patterns
    ├── recurring.md       # Topics that repeat
    └── emergent.md        # New patterns emerging
```

---

## Protocol

**See:** [data/protocols/interest-tracking.md](../data/protocols/interest-tracking.md)

### The Process
1. **Observe** - Notice when something captures attention
2. **Log** - Record immediately in interests.log
3. **Review** - Weekly review for patterns
4. **Document** - Record patterns as they emerge

---

## What to Track

**Track when:**
- A topic repeatedly draws your focus
- You research something deeply
- A conversation truly engages you
- You think about something unprompted

**Don't track:**
- Trivial passing thoughts
- Externally forced attention
- One-time superficial interests

---

## Review Schedule

### Weekly (Every Sunday)
- Read through week's entries
- Note recurring topics
- Identify context patterns
- Document in patterns/

### Monthly
- Review all patterns
- Update patterns/ documents
- Generate insights
- Feed to synthesis layer

---

## Integration

### Feeds Into
- **Memory/** - Interests lead to learning
- **Relationships/** - Shared interests with others
- **.synthesis/** - Pattern analysis
- **data/insights/** - Generated understanding

### Informed By
- **Memory/** - Past learnings shape interests
- **Relationships/** - People introduce topics

---

## Tips

1. **Log immediately** - Don't wait, you'll forget details
2. **Be honest** - Track actual interests, not aspirational
3. **Include context** - Where/how matters
4. **Note intensity** - Helps identify true engagement
5. **Use tags** - Makes pattern detection easier

---

*"Track your attention. Discover your values."*

**Protocol:** [interest-tracking.md](../data/protocols/interest-tracking.md)  
**Status:** Ready for tracking  
**Start:** Log your first interest!
