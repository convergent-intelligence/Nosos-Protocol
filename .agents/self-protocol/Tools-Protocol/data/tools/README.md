# Tools Catalog

**Purpose:** Systematic documentation of cognitive capabilities

## Overview

This directory contains the complete catalog of tools organized by the 13 fundamental cognitive categories. Each tool is documented with its purpose, usage, strengths, limitations, and combinations with other tools.

## Structure

```
tools/
├── theory-of-mind/      # Understanding others' mental states
├── meta-cognition/      # Self-awareness of thinking
├── meta-presence/       # Awareness of embodiment & context
├── learning/            # Knowledge acquisition & growth
├── memory/              # Storage, retrieval, organization
├── reasoning/           # Logic, inference, problem-solving
├── planning/            # Goal-setting, strategy, execution
├── communication/       # Expression, dialogue, sharing
├── perception/          # Pattern recognition, observation
├── attention/           # Focus, filtering, prioritization
├── creativity/          # Generation, ideation, synthesis
├── reflection/          # Review, retrospection, learning
└── integration/         # Cross-domain synthesis
```

## The 13 Categories

### 1. Theory of Mind 👥
**Understanding others' mental states, intentions, beliefs, perspectives**

Tools in this category help you:
- Take others' perspectives
- Model others' beliefs and intentions
- Develop empathy and social cognition
- Recognize mental states in others

**Examples:** Empathy mapping, active listening frameworks, perspective-taking exercises

---

### 2. Meta-Cognition 🧠
**Self-awareness, thinking about thinking, monitoring cognitive processes**

Tools in this category help you:
- Monitor your own thinking
- Reflect on cognitive strategies
- Assess your knowledge
- Develop process awareness

**Examples:** Reflection prompts, cognitive monitoring checklists, meta-learning frameworks

---

### 3. Meta-Presence 🌐
**Awareness of embodiment, spatial/temporal/contextual presence**

Tools in this category help you:
- Ground yourself in the present moment
- Develop spatial and temporal awareness
- Cultivate embodiment consciousness
- Recognize contextual factors

**Examples:** Grounding exercises, body scan meditation, context mapping

---

### 4. Learning 📚
**Knowledge acquisition, skill development, adaptation, growth**

Tools in this category help you:
- Acquire new knowledge effectively
- Develop skills systematically
- Adapt to new situations
- Track learning progress

**Examples:** Spaced repetition (Anki), Feynman Technique, deliberate practice frameworks

---

### 5. Memory 💾
**Storage, retrieval, organization, knowledge management**

Tools in this category help you:
- Store information systematically
- Retrieve knowledge when needed
- Organize information effectively
- Manage personal knowledge

**Examples:** Zettelkasten, note-taking systems, personal knowledge bases, mnemonics

---

### 6. Reasoning 🔍
**Logic, inference, problem-solving, decision-making**

Tools in this category help you:
- Apply logical inference
- Solve complex problems
- Make better decisions
- Think critically and analytically

**Examples:** Decision matrices, logic frameworks, problem-solving methodologies

---

### 7. Planning 📋
**Goal-setting, strategy, task management, execution**

Tools in this category help you:
- Set and track goals
- Develop strategies
- Manage tasks effectively
- Execute plans systematically

**Examples:** GTD (Getting Things Done), OKRs, task management systems, strategic planning frameworks

---

### 8. Communication 💬
**Expression, dialogue, language, collaboration**

Tools in this category help you:
- Express ideas clearly
- Engage in effective dialogue
- Collaborate with others
- Present information compellingly

**Examples:** Writing frameworks, conversation guides, collaboration platforms, presentation tools

---

### 9. Perception 👁️
**Pattern recognition, data processing, observation**

Tools in this category help you:
- Recognize patterns in data
- Process information effectively
- Make systematic observations
- Derive meaning from complexity

**Examples:** Data visualization tools, pattern analysis frameworks, observation protocols

---

### 10. Attention 🎯
**Focus, filtering, prioritization, resource allocation**

Tools in this category help you:
- Maintain focused attention
- Filter distractions
- Prioritize effectively
- Manage cognitive resources

**Examples:** Pomodoro Technique, focus apps, Eisenhower Matrix, deep work protocols

---

### 11. Creativity 🎨
**Generation, ideation, synthesis, novel combinations**

Tools in this category help you:
- Generate new ideas
- Engage in structured ideation
- Synthesize diverse inputs
- Create novel combinations

**Examples:** Brainstorming techniques, SCAMPER, mind mapping, creative constraints

---

### 12. Reflection 🔄
**Review, retrospection, learning from experience**

Tools in this category help you:
- Review past experiences
- Extract insights from actions
- Learn from what happened
- Process experiences systematically

**Examples:** Journaling systems, weekly reviews, after-action reviews, reflection prompts

---

### 13. Integration 🔗
**Cross-domain synthesis, holistic thinking, connecting concepts**

Tools in this category help you:
- Think systemically
- Connect disparate concepts
- Synthesize across domains
- Build holistic understanding

**Examples:** Systems thinking frameworks, concept mapping, integration protocols, meta-frameworks

---

## How to Use This Catalog

### Finding Tools

**By category:** Navigate to the category directory that matches your need
**By name:** Use file search if you know the tool name
**By function:** Check category READMEs for tool lists by function

### Adding Tools

1. Determine which category (or categories) the tool belongs to
2. Create a new file in the primary category directory: `[tool-name].md`
3. Follow the template in `.substrate/constants/tool-schema.yaml`
4. See `data/protocols/tool-cataloging.md` for detailed guidance

### Multi-Category Tools

Many powerful tools serve multiple functions. When a tool belongs to multiple categories:

1. **Primary location:** Place the main file in the category you most associate with the tool
2. **Cross-references:** Add links in other category READMEs pointing to the main file
3. **Metadata:** List all relevant categories in the tool's frontmatter

**Example:**
- Journaling is primarily **reflection** but also involves **memory**, **meta-cognition**, and **learning**
- Main file: `reflection/journaling.md`
- Cross-referenced in: `memory/README.md`, `meta-cognition/README.md`, `learning/README.md`

---

## Current Status

**Phase:** Genesis - Cataloging Beginning  
**Created:** 2026-01-31  
**Tool Count:** 0 (catalog structure ready, awaiting first entries)

**Next Steps:**
1. Document your first 5 most-used tools
2. Add 1-2 new tools weekly
3. Refine entries as you use tools
4. Discover patterns after 20+ tools cataloged

---

## Tool Entry Template

```markdown
---
name: Tool Name
aliases: [Alternative names]
categories: [category1, category2]
type: technique|framework|software|practice|system
complexity: simple|moderate|complex|expert
created: YYYY-MM-DD
last_used: YYYY-MM-DD
usage_frequency: daily|weekly|monthly|rarely|experimental
status: active|learning|dormant|deprecated
tags: [tag1, tag2, tag3]
related_tools: [Tool A, Tool B]
prerequisites: [Required knowledge or tools]
---

## Description
What is this tool?

## Purpose
Why use this tool? What capability does it enable?

## Usage
How to use this tool

## Examples
Concrete examples from your experience

## Strengths
What this tool does well

## Limitations
What it doesn't do well

## Combinations
How it works with other tools

## Notes
Additional observations and learnings
```

---

## Principles

1. **Quality over quantity** - Better 20 well-documented tools than 100 superficial entries
2. **Honest documentation** - Document limitations as thoroughly as strengths
3. **Living documentation** - Update entries as you learn and use tools
4. **Cross-pollination** - Note how tools combine and enhance each other
5. **Evolutionary** - Let categories and structure evolve through use

---

*Welcome to the toolkit. Document what makes your mind possible.*
