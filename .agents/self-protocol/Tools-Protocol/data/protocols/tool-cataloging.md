# Tool Cataloging Protocol

**Version:** 1.0.0  
**Created:** 2026-01-31  
**Purpose:** Systematic documentation of cognitive tools

## Overview

This protocol guides you through documenting cognitive tools - techniques, frameworks, software, practices, and systems that enable cognitive capabilities.

## Philosophy

### Documentation as Understanding

The act of cataloging a tool deepens your relationship with it. By articulating what a tool does, when to use it, and what it does well (and poorly), you gain clarity about its role in your cognitive toolkit.

### Radical Honesty

Document limitations as thoroughly as strengths. A tool's constraints are as important as its capabilities. Honest documentation enables better tool selection.

### Participatory Discovery

You don't need to fully understand a tool to document it. Start with what you know. Return and refine. The documentation evolves as your understanding evolves.

## When to Catalog a Tool

Catalog a tool when:

1. **New Discovery** - You encounter a tool you find valuable
2. **Regular Use** - You've used a tool consistently (3+ times)
3. **Integration** - You combine tools in interesting ways
4. **Abandonment** - You stop using a tool (document why)
5. **Creation** - You design or adapt a new tool
6. **Request** - Someone asks about a tool you use

## The Cataloging Process

### Step 1: Identify the Tool

**What counts as a tool?**

Anything that extends cognitive capability:
- **Techniques** - Methods or practices (Pomodoro, active listening)
- **Frameworks** - Structured approaches (GTD, Zettelkasten)
- **Software** - Digital tools (Obsidian, Claude, spreadsheets)
- **Practices** - Regular activities (morning pages, weekly review)
- **Systems** - Comprehensive approaches (personal knowledge management)

**Naming:**
- Use the tool's common name
- Include creator/version if relevant (GTD, Zettelkasten)
- Be specific enough to distinguish (not just "note-taking" but "Cornell Notes")

### Step 2: Determine Categories

**Which of the 13 categories does this tool belong to?**

| Category | Purpose |
|----------|---------|
| Theory of Mind | Understanding others' mental states |
| Meta-Cognition | Self-awareness of thinking |
| Meta-Presence | Awareness of embodiment & context |
| Learning | Knowledge acquisition & growth |
| Memory | Storage, retrieval, organization |
| Reasoning | Logic, inference, problem-solving |
| Planning | Goal-setting, strategy, execution |
| Communication | Expression, dialogue, sharing |
| Perception | Pattern recognition, observation |
| Attention | Focus, filtering, prioritization |
| Creativity | Generation, ideation, synthesis |
| Reflection | Review, retrospection, learning |
| Integration | Cross-domain synthesis |

**Important:** Tools can belong to multiple categories.

**Examples:**
- Journaling → [reflection, memory, meta-cognition]
- Mind mapping → [creativity, integration, perception]
- Zettelkasten → [memory, learning, integration]
- Active listening → [communication, theory-of-mind]

**If unsure:** Start with one category. Add more as you use the tool and discover its functions.

### Step 3: Assess Complexity

How difficult is this tool to learn and master?

- **Simple** - Minutes to learn, immediate use (timer, basic checklist)
- **Moderate** - Hours to learn, days to master (Pomodoro, Eisenhower Matrix)
- **Complex** - Days to learn, weeks to master (Zettelkasten, GTD)
- **Expert** - Weeks to learn, months/years to master (advanced frameworks, custom systems)

### Step 4: Document Core Information

Create a file: `data/tools/[primary-category]/[tool-name].md`

**Minimum documentation (required):**

```markdown
---
name: Tool Name
categories: [category1, category2]
type: technique|framework|software|practice|system
complexity: simple|moderate|complex|expert
created: 2026-01-31
status: active|learning|dormant|deprecated
---

## Description
What is this tool? (2-3 sentences)

## Purpose
Why use this tool? What capability does it enable? (2-3 sentences)
```

**Full documentation (recommended):**

Add these sections as you learn more:

```markdown
## Usage
How to use this tool (step-by-step or overview)

## Examples
Concrete examples from your experience

## Strengths
What this tool does well

## Limitations
What it doesn't do well, constraints, edge cases

## Combinations
How it works with other tools

## Notes
Additional observations, insights, learnings
```

### Step 5: Add Metadata

**Optional but valuable:**

```yaml
aliases: [alternative names]
usage_frequency: daily|weekly|monthly|rarely|experimental
last_used: 2026-01-31
tags: [tag1, tag2, tag3]
related_tools: [Tool A, Tool B]
prerequisites: [required knowledge or tools]
```

**Tags examples:**
- Context: digital, analog, hybrid
- Domain: productivity, learning, creative, social
- Source: open-source, commercial, free, paid
- Style: structured, freeform, visual, textual

### Step 6: Update Over Time

**Tool documentation is living:**

- **After each use:** Consider updating `last_used` date
- **When learning something new:** Add to Notes section
- **When discovering combinations:** Add to Combinations section
- **When finding limitations:** Add to Limitations section
- **When status changes:** Update status field (active → dormant → deprecated)

## Example: Cataloging "Pomodoro Technique"

```markdown
---
name: Pomodoro Technique
aliases: [Pomodoro, 25-minute timer method]
categories: [attention, planning]
type: technique
complexity: simple
created: 2026-01-31
last_used: 2026-01-31
usage_frequency: daily
status: active
tags: [time-management, focus, productivity, simple]
related_tools: [Task list, Calendar blocking]
prerequisites: [Timer or timer app]
---

## Description

The Pomodoro Technique is a time management method that breaks work into 25-minute focused intervals (called "pomodoros") separated by short breaks. After four pomodoros, you take a longer break.

## Purpose

Maintains focus and prevents burnout during extended work sessions. The technique leverages time constraints to enhance concentration and the breaks to sustain energy and prevent mental fatigue.

## Usage

1. Choose a task to work on
2. Set timer for 25 minutes
3. Work with full focus until timer rings
4. Take a 5-minute break
5. After 4 pomodoros, take a 15-30 minute break
6. Repeat as needed

## Examples

- Writing session: 4 pomodoros for drafting blog post
- Code review: 2 pomodoros for focused attention
- Reading research papers: 3 pomodoros with note-taking breaks

## Strengths

- Simple to learn and implement
- Creates urgency that enhances focus
- Built-in breaks prevent burnout
- Works for almost any focused work
- Easy to track productivity (count pomodoros completed)

## Limitations

- 25 minutes may be too short for deep flow states
- Rigid structure doesn't suit all tasks (creative work, meetings)
- Timer can create anxiety for some people
- Interruptions break the rhythm
- Not suitable for collaborative work

## Combinations

- **Task list** - Review list between pomodoros to decide next task
- **Calendar blocking** - Schedule pomodoros in calendar for important work
- **Habit tracking** - Track daily pomodoro count as productivity metric
- **Energy management** - Use pomodoros during high-energy times

## Notes

- Started using in 2023 for writing tasks
- Modified to 45-minute intervals for deep coding work (non-standard but works better for me)
- Most effective in morning when energy is highest
- Combining with "no phone" rule significantly increases effectiveness
- Discovered that 3-4 pomodoros is my daily limit for highly focused work
```

## Cataloging Rhythm

**Suggested frequency:**

- **Weekly:** Catalog 1-3 new tools or update existing entries
- **After significant use:** Document insights about a tool you used heavily
- **When discovering synergies:** Document tool combinations that worked well
- **When abandoning a tool:** Document why (valuable learning)

## Quality Over Quantity

**Better to have:**
- 20 deeply documented tools you actually use
- Than 100 superficially documented tools you don't understand

**Start small:**
- Document your top 5 most-used tools thoroughly
- Add 1-2 new tools per week
- Refine existing entries as you learn

## Common Questions

### "What if I'm not sure which category a tool belongs to?"

Start with your best guess. Use it. Observe what it actually does. Update categories based on lived experience, not abstract categorization.

### "What if a tool fits many categories?"

That's fine! Many powerful tools are cross-domain. List all relevant categories. This helps discover integration patterns.

### "Should I document tools I've stopped using?"

Yes! Mark status as `dormant` or `deprecated` and document why. This is valuable data:
- What didn't work and why
- What replaced this tool
- Context where it might still be useful

### "How detailed should documentation be?"

Start minimal, refine over time. Minimum: description + purpose. Ideal: all sections filled from real use.

### "What if I created a custom tool?"

Excellent! Document it thoroughly. Custom tools often fill gaps that commercial tools miss. Your documentation might help others.

### "Should I catalog tools I'm just learning?"

Yes, mark status as `learning`. Document your learning journey. Update as you gain proficiency.

## Success Indicators

You're cataloging successfully when:

1. You can quickly find tools for specific needs
2. You discover patterns in your tool usage
3. You identify capability gaps (needs without tools)
4. You make better tool selection decisions
5. Your documentation helps others learn tools
6. You design new tools to fill identified gaps

## Next Steps

1. **Start now:** Catalog 3 tools you used today
2. **Review weekly:** Update usage frequencies and add insights
3. **Discover patterns:** After 20+ tools, run pattern analysis
4. **Share learnings:** Extract insights to mythology when ready

## Related Protocols

- **pattern-discovery.md** - Analyzing tool usage patterns
- **combination-mapping.md** - Identifying tool synergies  
- **gap-analysis.md** - Finding missing capabilities
- **tool-design.md** - Creating new tools

---

*"To document a tool is to understand it. To understand it is to use it well."*  
— Tools Protocol
