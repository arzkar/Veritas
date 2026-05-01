# Veritas UI/UX Architecture Specification

## Investigative Interface Design for Autonomous Due Diligence

**Version:** 1.0
**Status:** MVP + Long-Term Product Vision
**Purpose:** UI/UX Architecture & Technical Interview Preparation

---

# Table of Contents

1. UI Philosophy
2. Why Veritas Should NOT Feel Like a Chatbot
3. Core UX Principles
4. High-Level User Journey
5. Main Dashboard Architecture
6. Upload Experience
7. Investigation Dashboard
8. PDF/Deck Viewer
9. Claim Inspection System
10. Evidence Explorer
11. Global Credibility Dashboard
12. Agent Trace Viewer
13. Investigation Timeline
14. Narrative Tension Graph
15. Real-Time Investigation Updates
16. Uncertainty Visualization
17. Color System & Information Density
18. UI State Management
19. Frontend Architecture
20. Why Next.js Was Chosen
21. Why PDF.js Was Chosen
22. Why React Flow Was Chosen
23. Realtime Architecture
24. MVP UI Scope
25. Long-Term Product Vision
26. Technical Tradeoffs
27. Final UX Philosophy

---

# 1. UI Philosophy

The Veritas interface should feel like:

```text
an investigative intelligence terminal
```

NOT:

```text
a consumer chatbot.
```

This distinction is extremely important.

Most modern AI products inherit the:

- conversational UI paradigm
- assistant metaphor
- “ask anything” interaction model

Veritas intentionally rejects this design language.

The user experience should instead communicate:

- institutional skepticism
- analytical rigor
- evidence traceability
- reasoning transparency
- uncertainty visibility

The user should feel like they are:

```text
operating an investigative system.
```

not:

```text
chatting with an assistant.
```

---

# 2. Why Veritas Should NOT Feel Like a Chatbot

Chatbot UIs create several problems for investigative systems.

## 2.1 Chat Interfaces Hide Reasoning Structure

Chat UIs flatten:

- evidence relationships
- contradiction chains
- state transitions
- investigative history

into:

```text
linear conversation.
```

This destroys traceability.

---

## 2.2 Chatbots Encourage False Certainty

Most chatbot interfaces implicitly suggest:

```text
The AI has already figured everything out.
```

But Veritas is fundamentally:

```text
an uncertainty-aware system.
```

The UI must expose:

- ambiguity
- unresolved claims
- weak evidence
- contradictory findings
- credibility decay

rather than hiding them.

---

## 2.3 Investigative Work Requires Navigation

Users need to:

- inspect claims
- trace evidence
- compare contradictions
- replay investigations
- audit reasoning

This requires:

```text
multi-panel analytical interfaces.
```

not message bubbles.

---

# 3. Core UX Principles

The Veritas UI follows several foundational principles.

---

## 3.1 Explainability First

Every major conclusion should be:

- inspectable
- traceable
- evidence-backed
- confidence-scored

Users should always be able to answer:

```text
“Why did the system believe this?”
```

---

## 3.2 Uncertainty Must Be Visible

The interface should explicitly show:

- confidence scores
- unresolved investigations
- weak evidence
- suspicious absence
- contradiction severity

The UI should NEVER imply:

```text
absolute certainty.
```

---

## 3.3 Investigation Is a Process

The system should visually communicate:

- evidence gathering
- research escalation
- contradiction discovery
- skepticism routing
- credibility revision

The user should feel:

```text
an investigation unfolding.
```

---

## 3.4 Information Density Matters

This is not a casual consumer application.

The interface should tolerate:

- dense information layouts
- analytical tables
- evidence panes
- trace visualizations
- graph relationships

The aesthetic should feel closer to:

- Bloomberg Terminal
- Palantir
- cybersecurity investigation dashboards
- intelligence analysis systems

than:

- ChatGPT
- Notion AI
- consumer productivity apps

---

# 4. High-Level User Journey

The intended user flow:

```text
Upload Pitch Deck
        ↓
Claim Extraction Begins
        ↓
Live Investigation Dashboard
        ↓
Evidence Retrieval
        ↓
Contradiction Discovery
        ↓
Credibility Decay
        ↓
Cross-Claim Synthesis
        ↓
Final Due Diligence Report
```

The experience should feel:

```text
alive and investigative.
```

rather than:

```text
submit → wait → receive answer.
```

---

# 5. Main Dashboard Architecture

The core dashboard should use a:

```text
multi-panel investigative layout.
```

Proposed structure:

```text
┌────────────────────────────────────────────┐
│ TOP BAR                                   │
│ Upload | Company | Credibility | Status   │
├──────────────┬────────────────┬───────────┤
│ LEFT PANEL   │ CENTER PANEL  │ RIGHT     │
│              │                │ PANEL     │
│ Claims       │ Deck Viewer    │ Evidence  │
│ Timeline     │ PDF Slides     │ Traces    │
│ Graph Nav    │ Highlights     │ Metrics   │
├──────────────┴────────────────┴───────────┤
│ BOTTOM INVESTIGATION TIMELINE             │
└────────────────────────────────────────────┘
```

This layout enables:

- contextual navigation
- simultaneous reasoning visibility
- evidence inspection
- claim traceability

---

# 6. Upload Experience

The upload interface should remain intentionally simple.

Primary action:

```text
Upload Pitch Deck
```

Possible metadata inputs:

- startup website
- founder name
- industry category
- funding stage

The upload flow should immediately transition into:

```text
live investigation mode.
```

rather than a static loading spinner.

---

# 7. Investigation Dashboard

The dashboard is the heart of Veritas.

Its job is to visualize:

- investigative progress
- evidence flow
- contradiction emergence
- credibility revision

The dashboard should behave like:

```text
an operational intelligence system.
```

Key components:

- deck viewer
- evidence explorer
- claim graph
- contradiction panel
- credibility metrics
- agent traces

---

# 8. PDF / Deck Viewer

The deck viewer should visually render:

- slides
- extracted claims
- highlighted metrics
- contradictions
- suspicious claims

Technology:

```text
PDF.js
```

Claims should appear as:

- highlighted overlays
- inline annotations
- clickable investigative entities

Example:

```text
“We reached $12M ARR”
```

highlighted directly on the slide.

This creates:

```text
source-grounded reasoning.
```

---

# 9. Claim Inspection System

When users click a highlighted claim:

a detailed inspection pane opens.

Example structure:

```text
CLAIM
------
“We reached $12M ARR”

STATUS
------
CONTRADICTED

CREDIBILITY
------
0.31

EVIDENCE
------
- External article suggests $3M ARR
- Team size inconsistent with scale
- Weak hiring footprint

SKEPTIC NOTES
------
Expected market visibility absent.
```

This becomes:

```text
interactive investigative reasoning.
```

---

# 10. Evidence Explorer

The Evidence Explorer is one of the most important trust-building components.

Users should inspect:

- URLs
- snippets
- authority scores
- timestamps
- retrieval origins
- contradiction directionality

Example:

```text
Source: SEC Filing
Authority: 0.98
Sentiment: Contradicts Claim
Recency: High
```

This reinforces:

```text
traceable evidence grounding.
```

---

# 11. Global Credibility Dashboard

The system should continuously display:

```text
Global Credibility Score
```

Example:

```text
42%
```

Additional metrics:

- contradiction count
- unresolved claims
- suspicious absence count
- strongest red flags
- investigation depth

This creates:

```text
continuous probabilistic assessment.
```

rather than binary conclusions.

---

# 12. Agent Trace Viewer

The Agent Trace Viewer exposes:

- reasoning summaries
- escalation paths
- retrieval decisions
- skepticism analysis
- synthesis logic

Example:

```text
Skeptic Agent:
Expected enterprise footprint absent.

Analyst Agent:
Revenue discrepancy exceeds expected tolerance.

Synthesis Agent:
Narrative coherence degraded.
```

This dramatically improves:

- trust
- explainability
- debugging
- interview/demo quality

---

# 13. Investigation Timeline

The system should expose:

```text
chronological investigation flow.
```

Example:

```text
Extractor
    ↓
Research Agent
    ↓
Contradiction Found
    ↓
Escalation Triggered
    ↓
Skeptic Review
    ↓
Credibility Updated
```

This makes the investigation feel:

```text
procedural and auditable.
```

---

# 14. Narrative Tension Graph

Long-term:

Veritas should visualize:

- claim dependencies
- contradiction chains
- credibility propagation
- narrative tensions

Example:

```text
Claim A ── weakens ── Claim B
      │
      └── contradicts ── Claim C
```

Technology:

```text
React Flow
```

This graph becomes:

```text
visualized probabilistic reasoning.
```

---

# 15. Real-Time Investigation Updates

The dashboard should update live.

Users should watch:

- claims extracted
- evidence retrieved
- contradictions discovered
- credibility scores change

This creates:

```text
AI investigation in progress.
```

Realtime updates improve:

- engagement
- transparency
- trust
- perceived intelligence

---

# 16. Uncertainty Visualization

This is one of the most important UX requirements.

The UI should visually distinguish:

- verified claims
- contradicted claims
- unresolved claims
- suspiciously absent evidence
- low-confidence analysis

Possible methods:

- opacity
- warning colors
- uncertainty badges
- confidence bars
- ambiguity indicators

The system should normalize:

```text
visible uncertainty.
```

rather than hiding it.

---

# 17. Color System & Information Density

Recommended visual style:

- dark analytical UI
- minimal gradients
- restrained accent colors
- high information density
- subtle motion

Suggested palette:

| Meaning             | Color  |
| ------------------- | ------ |
| Verified            | Green  |
| Contradicted        | Red    |
| Unresolved          | Yellow |
| Suspiciously Absent | Orange |
| Escalated           | Purple |

The UI should feel:

```text
institutional and operational.
```

not playful.

---

# 18. UI State Management

Frontend state complexity will become significant.

The UI must manage:

- live graph updates
- claim transitions
- evidence streams
- websocket events
- investigation traces

Recommended:

```text
Zustand
```

Reasons:

- lightweight
- simple mental model
- excellent React integration
- avoids Redux complexity

---

# 19. Frontend Architecture

Recommended stack:

| Purpose             | Technology  |
| ------------------- | ----------- |
| Frontend Framework  | Next.js     |
| Styling             | TailwindCSS |
| Components          | shadcn/ui   |
| PDF Rendering       | PDF.js      |
| Graph Visualization | React Flow  |
| State Management    | Zustand     |
| Realtime Updates    | WebSockets  |

This stack optimizes for:

- rapid iteration
- flexibility
- developer experience
- modern React ecosystem compatibility

---

# 20. Why Next.js Was Chosen

Next.js provides:

- excellent React ecosystem support
- routing simplicity
- API integration flexibility
- modern frontend tooling
- strong TypeScript support

It is ideal for:

```text
analytical dashboard applications.
```

---

# 21. Why PDF.js Was Chosen

Pitch decks are the primary investigative surface.

PDF.js enables:

- accurate rendering
- annotation overlays
- slide navigation
- zooming
- embedded interaction layers

The deck viewer is not optional.

It is:

```text
the primary evidence surface.
```

---

# 22. Why React Flow Was Chosen

React Flow is ideal for:

- graph visualization
- relationship tracing
- contradiction mapping
- investigation topology

This enables:

```text
visualized reasoning structures.
```

which become extremely valuable later.

---

# 23. Realtime Architecture

Realtime updates should use:

```text
WebSockets
```

Reasons:

- live investigation progress
- incremental claim updates
- evidence streaming
- credibility score changes

Polling would create:

- poor responsiveness
- inefficient updates
- delayed investigative feedback

Realtime interaction reinforces:

```text
procedural intelligence.
```

---

# 24. MVP UI Scope

The MVP should intentionally remain small.

Required:

- upload page
- deck viewer
- highlighted claims
- evidence sidebar
- credibility dashboard
- final synthesis report

Not required initially:

- graph visualization
- collaborative investigation
- portfolio dashboards
- complex animations
- advanced replay systems

The MVP should prioritize:

```text
reasoning visibility over visual complexity.
```

---

# 25. Long-Term Product Vision

Long-term:

Veritas could evolve into:

```text
an AI-powered investigative terminal.
```

Potential future features:

- portfolio-wide analysis
- founder relationship graphs
- startup intelligence memory
- fraud similarity detection
- collaborative analyst workspaces
- historical credibility tracking

The interface may eventually resemble:

- Palantir
- Bloomberg Terminal
- cyber threat intelligence dashboards

But focused on:

```text
startup credibility analysis.
```

---

# 26. Technical Tradeoffs

Every UI decision introduces tradeoffs.

---

## High Information Density

Pros:

- analyst efficiency
- better traceability
- more transparency

Cons:

- steeper learning curve
- less consumer-friendly

---

## Realtime Investigations

Pros:

- engaging
- transparent
- inspectable

Cons:

- more backend complexity
- websocket state synchronization

---

## Explainability-Focused UX

Pros:

- trust
- auditability
- interview value

Cons:

- more interface complexity
- more engineering overhead

These tradeoffs are intentional.

---

# 27. Final UX Philosophy

The Veritas UI should communicate:

```text
institutional skepticism as software.
```

The user should feel:

- informed
- investigative
- analytical
- empowered to inspect

The system should never feel:

- magical
- opaque
- overconfident
- chatbot-like

The interface itself becomes part of the trust model.

Veritas succeeds when users feel:

```text
“I can inspect the reasoning process.”
```

rather than:

```text
“The AI simply told me the answer.”
```

That distinction is the foundation of the entire UX philosophy.

---

# Final Technical Summary

## Core UI Goals

- explainability
- traceability
- uncertainty visibility
- evidence inspection
- investigative flow visualization

---

## Core Technologies

- Next.js
- TailwindCSS
- shadcn/ui
- PDF.js
- React Flow
- Zustand
- WebSockets

---

## Core UX Philosophy

```text
Not a chatbot.
An investigative intelligence system.
```

---

_End of Veritas UI/UX Architecture Specification_
