# Veritas: The Investigative Operating System for Autonomous Due Diligence

## Expanded Technical Whitepaper, Systems Design Deep-Dive & Interview Preparation Document

**Version:** 2.0.0-EXPANDED
**Status:** Technical Interview Preparation Draft
**Author:** Veritas Engineering
**Date:** May 12, 2026

---

# Table of Contents

1. Executive Summary
2. Why Veritas Exists
3. The Fundamental Problem With AI Due Diligence
4. Why Traditional RAG Fails
5. Architectural Philosophy
6. Epistemology as a Systems Design Primitive
7. Why Veritas is an Uncertainty Management System
8. High-Level System Architecture
9. Multi-Agent Systems Philosophy
10. Why LangGraph Was Chosen
11. Why Python Was Chosen
12. Why Local-First Development Was Chosen
13. Why Qwen3 8B Was Chosen
14. Why FAISS Was Chosen
15. Why Pydantic Was Chosen
16. The Claim Object as the Core Primitive
17. Epistemic State Machine Design
18. Evidence Modeling
19. Global Credibility Propagation
20. Bayesian Credibility Revision
21. The Skeptic Agent
22. The Synthesis Agent
23. Investigative Orchestration
24. Retrieval Architecture
25. Multimodal Escalation Strategy
26. Observability & Traceability
27. Evaluation Methodology
28. Cost Optimization Strategy
29. Failure Modes & Reliability Engineering
30. Security Threat Model
31. Scaling Considerations
32. Technical Tradeoffs
33. Why This Architecture Matters
34. Future Evolution of Veritas
35. Closing Thoughts

---

# 1. Executive Summary

Veritas is a stateful, adversarial, uncertainty-aware autonomous due diligence platform designed to investigate startup pitch decks.

Unlike traditional AI systems that optimize for:

- coherence
- summarization
- conversational helpfulness
- passive retrieval

Veritas optimizes for:

- contradiction discovery
- evidence grounding
- adversarial reasoning
- credibility modeling
- uncertainty propagation
- investigative traceability

The system treats startup narratives as:

```text
Untrusted probabilistic claims.
```

rather than:

```text
Sources of truth.
```

This philosophical shift fundamentally changes the architecture.

Veritas is not a chatbot.

It is not a generic RAG pipeline.

It is not a PDF summarizer.

It is an:

```text
Investigative Operating System.
```

The primary objective of Veritas is to calculate:

```text
The credibility delta between narrative and reality.
```

This is accomplished through:

- claim extraction
- external evidence retrieval
- contradiction analysis
- skepticism heuristics
- credibility decay
- global belief revision

The system continuously updates a probabilistic belief model about the reliability of the startup itself.

This document explains not only:

- what Veritas does

but also:

- why every architectural decision was made
- which tradeoffs were accepted
- how uncertainty is represented structurally
- how multi-agent orchestration is implemented
- how the system scales cognitively and operationally

---

# 2. Why Veritas Exists

The modern startup ecosystem has an asymmetry problem.

Founders can:

- spend months refining a narrative
- selectively present metrics
- optimize visual persuasion
- hide uncertainty
- exaggerate traction
- manipulate framing

Meanwhile:

- investors operate under time pressure
- analysts manually validate claims
- diligence cycles are expensive
- contradictions are easy to miss
- information is fragmented across the internet

Traditional due diligence is:

- labor intensive
- repetitive
- inconsistent
- difficult to scale

The rise of AI created an opportunity to automate parts of this process.

However:

most AI systems are fundamentally designed to:

```text
assist users.
```

Veritas intentionally rejects this design assumption.

The system is built around:

```text
institutional skepticism.
```

That changes:

- prompting
- orchestration
- retrieval
- scoring
- memory
- evaluation
- state design

The central question becomes:

```text
“How believable is this company narrative under external scrutiny?”
```

rather than:

```text
“What did the PDF say?”
```

---

# 3. The Fundamental Problem With AI Due Diligence

Most AI diligence systems accidentally create:

```text
The Circular Trust Trap.
```

Example:

1. Startup claims:

```text
“We hit $15M ARR.”
```

2. AI retrieves the claim from the PDF.

3. AI repeats:

```text
“The company achieved $15M ARR.”
```

This is not verification.

It is:

```text
Narrative amplification.
```

The system never challenged the claim.

It merely rephrased it.

This happens because traditional RAG systems assume:

```text
retrieved context = truth.
```

That assumption is catastrophic in adversarial domains.

Especially:

- venture capital
- compliance
- security
- fraud detection
- financial analysis

Veritas solves this by enforcing:

```text
zero-trust ingestion.
```

Every extracted statement enters the system as:

```text
UNVERIFIED
```

until proven otherwise.

---

# 4. Why Traditional RAG Fails

Traditional Retrieval-Augmented Generation architectures are optimized for:

- question answering
- semantic retrieval
- contextual completion
- summarization

These architectures fail under adversarial information environments because:

## 4.1 They Trust Context Too Easily

RAG assumes:

```text
retrieved information is authoritative.
```

But startup decks are persuasion artifacts.

Not evidence repositories.

---

## 4.2 They Lack Epistemic States

Most systems have:

```text
found / not found
```

Veritas instead models:

- supported
- contradicted
- unresolved
- suspiciously absent
- ambiguous
- escalated

This creates:

```text
uncertainty-aware reasoning.
```

---

## 4.3 They Lack Adversarial Intent

Traditional systems attempt to:

```text
answer questions.
```

Veritas attempts to:

```text
challenge narratives.
```

This distinction changes:

- prompts
- retrieval
- orchestration
- evaluation
- output formatting

---

# 5. Architectural Philosophy

The architecture follows several foundational principles.

## 5.1 Uncertainty Must Be Explicit

The system should never imply certainty where uncertainty exists.

Every output should carry:

- confidence
- ambiguity
- evidence quality
- credibility weighting

---

## 5.2 Agent Outputs Are Not Truth

LLM generations are:

- probabilistic
- fallible
- revisable
- context-dependent

Therefore:

agent outputs should be treated as:

```text
investigative hypotheses.
```

not:

```text
facts.
```

---

## 5.3 State Matters More Than Prompts

Most AI demos focus excessively on prompts.

Veritas prioritizes:

- schemas
- orchestration
- state transitions
- evidence grounding
- belief propagation

The prompt is only one component.

The real system is:

```text
the epistemic graph.
```

---

## 5.4 The System Must Be Comfortable Saying:

```text
“We do not know.”
```

This is critical.

Many AI systems hallucinate certainty.

Veritas intentionally preserves:

- ambiguity
- unresolved contradictions
- incomplete investigations

because uncertainty itself is valuable signal.

---

# 6. Epistemology as a Systems Design Primitive

One of the most important architectural decisions in Veritas is:

```text
uncertainty is encoded structurally.
```

not hidden inside natural language.

This means:

- schemas represent uncertainty
- state transitions represent investigation progress
- evidence carries trust metrics
- claims carry credibility weights

The system therefore behaves more like:

```text
a probabilistic investigation engine
```

than:

```text
a conversational assistant.
```

This design dramatically improves:

- debuggability
- observability
- orchestration reliability
- evaluation quality
- reproducibility

---

# 7. Why Veritas is an Uncertainty Management System

This became the defining architectural realization.

Veritas is not fundamentally:

- a retrieval system
- a chatbot
- a summarizer
- a parser

It is fundamentally:

```text
an uncertainty management system.
```

The core task is:

```text
continuously updating confidence in a startup narrative.
```

This changes:

- how evidence is weighted
- how contradictions propagate
- how retrieval loops behave
- how agents communicate
- how synthesis occurs

The system continuously asks:

```text
“How much should we believe this company?”
```

rather than:

```text
“What information did we retrieve?”
```

---

# 8. High-Level System Architecture

```text
PDF Upload
    ↓
Ingestion Pipeline
    ↓
Claim Extraction
    ↓
Parallel Investigation Threads
    ↓
Research Agent
    ↓
Analyst Agent
    ↓
Skeptic Agent
    ↓
Cross-Claim Synthesis
    ↓
Global Credibility Revision
    ↓
Final Diligence Report
```

The architecture intentionally separates:

- extraction
- retrieval
- contradiction analysis
- skepticism
- synthesis

This improves:

- modularity
- observability
- debugging
- parallelization
- reliability

---

# 9. Multi-Agent Systems Philosophy

A critical clarification:

```text
multi-agent does NOT mean multiple models.
```

In Veritas:

agents are primarily:

- orchestration roles
- prompt specializations
- tool-access policies
- state-aware behaviors

The same reasoning model may power:

- Extractor
- Researcher
- Analyst
- Skeptic
- Synthesizer

This architecture is:

- cheaper
- more debuggable
- easier to calibrate
- easier to observe

The intelligence emerges from:

```text
workflow structure.
```

not from using many giant models.

---

# 10. Why LangGraph Was Chosen

LangGraph was selected because Veritas is not a linear pipeline.

The workflow contains:

- retries
- escalations
- branching
- loops
- reflection
- stateful transitions

Standard chains are insufficient.

Veritas requires:

```text
cyclical investigative orchestration.
```

Examples:

- Analyst detects contradiction
- Research confidence is weak
- System loops back into targeted retrieval

This is fundamentally:

```text
graph behavior.
```

not sequential execution.

---

# 11. Why Python Was Chosen

Python dominates:

- LLM tooling
- vector databases
- orchestration frameworks
- ML infrastructure
- embeddings ecosystems

Critical libraries:

- LangGraph
- FastAPI
- Pydantic
- FAISS
- sentence-transformers
- HuggingFace

The ecosystem maturity makes Python the obvious choice.

Additionally:

Python excels at:

- rapid iteration
- experimentation
- async APIs
- agent orchestration

which aligns directly with Veritas requirements.

---

# 12. Why Local-First Development Was Chosen

Veritas intentionally follows:

```text
local-first AI development.
```

Reasons:

- lower cost
- reproducibility
- offline experimentation
- observability
- faster iteration
- reduced API dependency

This architecture also prevents:

```text
premature cloud complexity.
```

The MVP should optimize for:

- learning velocity
- orchestration quality
- schema stability

not production hyperscaling.

---

# 13. Why Qwen3 8B Was Chosen

Qwen3 8B provides:

- strong structured outputs
- good reasoning
- excellent local performance
- tool-call compatibility
- efficient inference on Apple Silicon

The model is sufficiently capable for:

- extraction
- orchestration
- skepticism
- contradiction analysis

without requiring expensive cloud infrastructure.

This aligns with the philosophy that:

```text
architecture matters more than parameter count.
```

---

# 14. Why FAISS Was Chosen

FAISS was selected because it is:

- local
- fast
- lightweight
- highly mature
- cost-free

The MVP does not require:

- distributed vector infrastructure
- managed retrieval services
- hyperscale indexing

FAISS enables:

- rapid experimentation
- ephemeral session indexes
- local debugging
- deterministic retrieval flows

This dramatically simplifies development.

---

# 15. Why Pydantic Was Chosen

Pydantic is critical because Veritas depends heavily on:

```text
structured epistemology.
```

Every agent communicates using:

- typed schemas
- validated objects
- deterministic state transitions

This prevents:

- schema drift
- malformed outputs
- orchestration instability
- inconsistent evidence structures

Pydantic effectively becomes:

```text
the contract layer of the investigation system.
```

---

# 16. The Claim Object as the Core Primitive

The Claim Object is the single most important abstraction in Veritas.

Everything revolves around claims.

A claim is:

```text
an investigative thread.
```

Claims move through:

- extraction
- research
- skepticism
- synthesis
- credibility revision

The entire architecture becomes significantly clearer once:

```text
the claim lifecycle becomes the primary state machine.
```

This was a critical architectural breakthrough.

---

# 17. Epistemic State Machine Design

Traditional systems use binary truth.

Veritas uses:

- supported
- contradicted
- unresolved
- suspiciously absent
- ambiguous

This creates:

```text
gradient reasoning.
```

instead of:

```text
binary certainty.
```

This is essential because startup investigations often contain:

- incomplete evidence
- conflicting signals
- asymmetric information
- unverifiable claims

The state machine therefore models:

```text
belief progression.
```

not:

```text
static truth.
```

---

# 18. Evidence Modeling

Evidence is treated as:

```text
an anchor to external reality.
```

Every evidence object carries:

- source authority
- recency
- relevance
- directional impact
- sentiment strength

This allows:

- weighted reasoning
- credibility propagation
- confidence calibration

Different evidence types have different trust levels.

Example:

- SEC filing > anonymous forum post
- audited report > startup blog

This prevents:

```text
flat trust assumptions.
```

---

# 19. Global Credibility Propagation

One of the most important design decisions:

```text
credibility damage is asymmetric.
```

A strong validation:

- slightly increases trust.

A severe contradiction:

- massively decreases trust.

This mirrors real human diligence behavior.

Example:

If a startup lies about:

- revenue
- customers
- founder background

then:

all unresolved claims become more suspicious.

This creates:

```text
belief propagation across the investigative graph.
```

---

# 20. Bayesian Credibility Revision

The global credibility engine continuously updates:

```text
P(company narrative is reliable)
```

based on:

- contradiction severity
- evidence strength
- claim importance
- uncertainty

This is effectively:

```text
Bayesian belief revision.
```

The system continuously updates:

```text
its prior assumptions.
```

about the company.

This creates:

```text
dynamic skepticism.
```

rather than static scoring.

---

# 21. The Skeptic Agent

The Skeptic Agent is the defining differentiator of Veritas.

Most AI systems are optimized for:

```text
agreement.
```

The Skeptic is optimized for:

```text
disbelief.
```

Its purpose is not merely contradiction.

Its purpose is:

- finding missing evidence
- detecting impossible narratives
- identifying suspicious absence
- amplifying weak signals

The Skeptic behaves more like:

```text
a forensic auditor.
```

than:

```text
a conversational assistant.
```

---

# 22. The Synthesis Agent

The Synthesis Agent is the most holistic reasoning component.

Its job is not merely:

```text
fact matching.
```

Its job is:

```text
narrative coherence evaluation.
```

It searches for:

- strategic inconsistency
- operational impossibility
- business model tension
- compounding credibility erosion

This mirrors how senior investors actually reason.

Humans rarely reject startups because of:

```text
one isolated metric.
```

They reject startups because:

```text
the story stops making sense.
```

---

# 23. Investigative Orchestration

Each claim initially becomes:

```text
an isolated micro-investigation.
```

This improves:

- parallelism
- reasoning clarity
- retry isolation
- observability

Later:

claims converge into:

```text
cross-claim synthesis.
```

This hybrid approach avoids:

- context dilution
- monolithic prompts
- retrieval contamination

while preserving:

```text
global narrative reasoning.
```

---

# 24. Retrieval Architecture

Retrieval is intentionally separated into:

- semantic retrieval
- benchmark retrieval
- evidence retrieval
- metadata filtering

The retrieval layer is not merely:

```text
search.
```

It is:

```text
reality grounding infrastructure.
```

This distinction matters enormously.

---

# 25. Multimodal Escalation Strategy

Pitch decks are visual reasoning artifacts.

However:

full multimodal processing is expensive.

Veritas therefore uses:

```text
cost-aware multimodal escalation.
```

The system only escalates visually ambiguous slides.

Examples:

- tables
- KPI graphs
- competitor matrices
- infographic-heavy slides

This dramatically reduces:

- cost
- latency
- unnecessary vision inference

while preserving:

```text
high-value visual extraction.
```

---

# 26. Observability & Traceability

Observability is mandatory.

Without observability:

- debugging becomes impossible
- hallucinations become invisible
- agent loops become opaque

The system therefore logs:

- prompts
- tool calls
- evidence references
- credibility transitions
- orchestration paths
- retries
- failures

This creates:

```text
investigative traceability.
```

Every contradiction should be explainable.

---

# 27. Evaluation Methodology

Evaluation is one of the hardest components.

The system cannot simply be evaluated on:

```text
text generation quality.
```

Instead evaluation must measure:

- contradiction accuracy
- uncertainty calibration
- hallucination resistance
- evidence quality
- credibility propagation
- reasoning consistency

This requires:

- synthetic decks
- seeded contradictions
- adversarial test cases
- human-reviewed investigations

---

# 28. Cost Optimization Strategy

Cost optimization is architectural.

The system intentionally uses:

- local inference
- selective multimodal escalation
- bounded research budgets
- metadata-only graph states

This prevents:

- context explosion
- runaway token costs
- uncontrolled recursive loops

The system behaves more like:

```text
a bounded investigation.
```

than:

```text
an infinite search process.
```

---

# 29. Failure Modes & Reliability Engineering

The system explicitly models:

- unresolved ambiguity
- failed retrieval
- low-confidence extraction
- contradictory evidence

Failure itself becomes:

```text
a meaningful state.
```

This dramatically improves robustness.

The system should fail:

```text
gracefully and transparently.
```

rather than hallucinating certainty.

---

# 30. Security Threat Model

The architecture assumes:

```text
adversarial inputs.
```

Possible attacks include:

- prompt injection in PDFs
- misleading metrics
- SEO manipulation
- fake evidence generation
- reputation laundering

Therefore:

- evidence weighting
- domain authority
- retrieval validation
- graph isolation

become critical security primitives.

---

# 31. Scaling Considerations

The MVP intentionally avoids:

- microservices
- Kubernetes complexity
- distributed orchestration

because:

premature scale destroys iteration speed.

The architecture is designed to scale later through:

- graph partitioning
- retrieval sharding
- asynchronous orchestration
- specialized agent routing

---

# 32. Technical Tradeoffs

Every architecture decision introduces tradeoffs.

Examples:

## Local Models

Pros:

- cheap
- observable
- reproducible

Cons:

- weaker reasoning ceiling
- weaker multimodal capabilities

---

## Parallel Claim Processing

Pros:

- cleaner reasoning
- scalability
- isolation

Cons:

- cross-claim relationships emerge later

---

## Selective Vision Escalation

Pros:

- lower cost
- faster processing

Cons:

- possible missed visual nuance

Tradeoffs are intentional.

---

# 33. Why This Architecture Matters

Most AI products today are:

```text
interface wrappers around LLM APIs.
```

Veritas attempts something deeper.

It attempts to build:

```text
structured investigative cognition.
```

The real innovation is not:

- the UI
- the prompt
- the model

The innovation is:

- epistemic orchestration
- uncertainty propagation
- credibility revision
- adversarial reasoning

This creates a fundamentally different class of AI system.

---

# 34. Future Evolution of Veritas

Long-term:

Veritas may evolve toward:

```text
probabilistic investigative graph reasoning.
```

Future capabilities may include:

- portfolio-level intelligence
- founder credibility history
- market graph analysis
- fraud similarity detection
- autonomous diligence escalation
- temporal credibility tracking

The architecture already hints at:

```text
persistent organizational memory.
```

---

# 35. Closing Thoughts

Veritas represents a shift away from:

```text
AI as conversational assistance.
```

toward:

```text
AI as structured epistemic infrastructure.
```

The system is fundamentally designed around:

- skepticism
- uncertainty
- evidence
- traceability
- belief revision

The most important realization throughout the architecture process was:

```text
Veritas is not evaluating isolated claims.
```

It is:

```text
continuously updating a probabilistic belief model about the reliability of the startup itself.
```

That realization shaped:

- state design
- orchestration
- evidence modeling
- credibility scoring
- synthesis logic
- retrieval strategy
- evaluation methodology

Ultimately:

Veritas is an attempt to engineer:

```text
institutional skepticism as software.
```

---

# Final Technical Summary

## Core Stack

- Python
- FastAPI
- LangGraph
- Pydantic
- FAISS
- Ollama
- Qwen3 8B
- nomic-embed-text

---

## Core Concepts

- uncertainty-aware orchestration
- adversarial reasoning
- epistemic state machines
- credibility propagation
- bounded investigations
- evidence grounding
- investigative traceability

---

## Core Philosophy

```text
Trust nothing.
Track uncertainty.
Ground everything.
Question the narrative.
```

---

_End of Expanded Technical Whitepaper_
_Prepared for Systems Design & AI Infrastructure Interviews_
_Veritas Engineering Specification v2.0_
