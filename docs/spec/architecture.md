# Veritas — Specification Files Bundle

This document contains the initial `.md` specification files for the Veritas project.

---

# `/specs/architecture.md`

````md
# Veritas Architecture Specification

## Overview

Veritas is a multi-agent AI due diligence platform designed to:

- analyze startup pitch decks
- validate business claims
- retrieve external market evidence
- detect contradictions
- generate investment risk reports

The system follows an agentic workflow architecture instead of a standard chatbot pipeline.

---

# Core Principles

## 1. Never Trust Claims Blindly

Every startup claim is considered unverified until:

- external evidence supports it
- internal consistency checks pass
- confidence scoring succeeds

---

## 2. Tool Usage is Mandatory

Agents must actively use tools.

Examples:

- web search
- vector retrieval
- GitHub lookup
- company intelligence APIs
- market report retrieval

This is NOT a static RAG system.

---

## 3. Structured Outputs Everywhere

Every agent must return structured JSON/Pydantic objects.

Avoid:

- raw prose outputs
- inconsistent formatting
- ambiguous data structures

---

# High-Level Architecture

```text
User Uploads Pitch Deck
           ↓
     PDF Processing Layer
           ↓
      Extractor Agent
           ↓
         Claim DB
           ↓
      Research Agent
           ↓
    External Data Sources
           ↓
       Analyst Agent
           ↓
       Skeptic Agent
           ↓
        Final Report
```
````

---

# System Components

## API Layer

Responsible for:

- file uploads
- orchestration requests
- report retrieval
- session tracking

Tech:

- FastAPI

---

## Agent Layer

Responsible for:

- reasoning
- tool usage
- verification
- analysis

Framework Options:

- LangGraph
- LangChain
- PydanticAI

---

## Retrieval Layer

Responsible for:

- embeddings
- vector search
- metadata filtering
- semantic retrieval

Database Options:

- FAISS
- Chroma

---

## Tool Layer

Responsible for:

- web search
- GitHub inspection
- market intelligence
- financial data retrieval

---

## Observability Layer

Responsible for:

- prompt tracing
- latency tracking
- token usage
- retry monitoring
- tool visibility

---

# Core Workflow

## Step 1 — Ingestion

PDF uploaded.

System extracts:

- text
- slide structure
- tables
- charts metadata

---

## Step 2 — Claim Extraction

Extractor Agent identifies:

- growth claims
- market size claims
- funding statements
- partnerships
- traction metrics

Claims become structured objects.

---

## Step 3 — Research

Research Agent:

- generates search queries
- retrieves evidence
- ranks relevance
- summarizes findings

---

## Step 4 — Contradiction Analysis

Analyst Agent compares:

- startup claims
- external evidence
- internal consistency

Flags:

- exaggeration
- unsupported metrics
- suspicious claims

---

## Step 5 — Adversarial Review

Skeptic Agent attempts to disprove:

- traction
- technical capability
- market dominance
- financial assumptions

---

## Step 6 — Final Report

Generate:

- confidence score
- red flags
- diligence summary
- investment memo

---

# Non-Goals

Veritas is NOT:

- a chatbot
- a general-purpose assistant
- a simple PDF summarizer
- a generic RAG application

---

# MVP Constraints

Initial version should:

- support only PDF decks
- use English-only analysis
- support only async report generation
- avoid real-time streaming complexity

---

# Long-Term Vision

Future capabilities:

- multi-document analysis
- portfolio-wide intelligence
- startup graph relationships
- investor memory system
- fraud probability scoring
- autonomous investment recommendations

````

---

# `/specs/agents.md`

```md
# Veritas Agent Specification

# Agent Philosophy

Agents are specialized workers.

Each agent:

- has a narrow responsibility
- owns specific tools
- returns structured outputs
- communicates through shared state

Avoid "god agents".

---

# Agent List

| Agent | Responsibility |
|---|---|
| Extractor | Extract claims from documents |
| Researcher | Gather external evidence |
| Analyst | Compare evidence and claims |
| Skeptic | Attempt to disprove findings |
| Report Agent | Generate final memo |

---

# Extractor Agent

## Goal

Convert raw pitch deck text into structured claims.

---

## Inputs

- parsed PDF chunks
- slide metadata

---

## Outputs

```json
{
  "claim_id": "clm_001",
  "category": "market_share",
  "statement": "We own 40% of the European fintech market.",
  "confidence": 0.84,
  "slide": 8
}
````

---

## Rules

Extractor MUST:

- ignore marketing fluff
- ignore opinions
- focus on objective claims
- avoid hallucinating metrics

---

# Researcher Agent

## Goal

Verify claims using external sources.

---

## Tools

- Tavily
- Serper
- GitHub API
- Vector DB
- Company APIs

---

## Responsibilities

### Generate Search Queries

Example:

Claim:

```text
Largest AI accounting startup in India.
```

Generated Queries:

```text
Largest AI accounting startups India
Top accounting SaaS India 2026
Indian bookkeeping AI startups funding
```

---

## Evidence Requirements

Every evidence item must include:

- source
- snippet
- confidence
- timestamp
- URL

---

# Analyst Agent

## Goal

Detect inconsistencies.

---

## Examples

### Contradiction

Claim:

```text
40% market share
```

Evidence:

```text
Competitors dominate 90% of market.
```

Result:

```json
{
  "status": "contradiction_detected"
}
```

---

## Responsibilities

- identify conflicts
- estimate credibility
- produce risk summaries
- score evidence quality

---

# Skeptic Agent

## Goal

Act adversarially.

Purpose:

- challenge assumptions
- stress-test conclusions
- search for missing evidence

---

## Example Questions

- Is this growth mathematically possible?
- Is the TAM inflated?
- Is this team large enough?
- Is GitHub activity suspiciously low?

---

# Report Agent

## Goal

Generate final VC-style memo.

---

## Sections

- Executive Summary
- Market Analysis
- Risks
- Contradictions
- Technical Assessment
- Final Confidence Score

---

# Agent Communication

Agents communicate via:

- shared state
- structured schemas
- orchestration graph

Avoid direct prompt-to-prompt freeform communication.

---

# Failure Handling

If an agent fails:

- retry once
- log failure
- degrade gracefully
- continue pipeline where possible

---

# Reflection Loops

Future versions may include:

- self-critique
- confidence re-evaluation
- secondary evidence retrieval

````

---

# `/specs/retrieval.md`

```md
# Retrieval & Vector Database Specification

# Overview

The retrieval layer powers:

- semantic search
- contextual memory
- evidence retrieval
- historical comparison

---

# Embedding Strategy

## Local Embeddings Preferred

Initial implementation:

```text
all-MiniLM-L6-v2
````

Reasons:

- free
- fast
- CPU-friendly
- low-latency

---

# Chunking Strategy

## Primary Chunking

Chunk by:

- slide
- semantic section
- table boundaries

Avoid naive fixed-token chunking.

---

# Metadata Requirements

Each chunk MUST include:

```json
{
  "document_id": "deck_001",
  "slide": 7,
  "chunk_type": "traction",
  "company": "AcmeAI"
}
```

---

# Vector Database

## Initial Choice

FAISS

Reasons:

- local
- fast
- free
- easy experimentation

---

# Retrieval Flow

```text
User Query
    ↓
Embedding Generation
    ↓
Vector Search
    ↓
Metadata Filtering
    ↓
Reranking
    ↓
Relevant Context
```

---

# Retrieval Types

## Semantic Retrieval

Find conceptually similar information.

---

## Metadata Filtering

Example:

```text
Only search:
- competitor analysis
- fintech reports
- documents from 2026
```

---

## Hybrid Retrieval

Combine:

- semantic search
- keyword search
- metadata filters

---

# Reranking

Future optimization:

Use reranking models to:

- reduce hallucinations
- improve evidence quality
- improve relevance precision

---

# Long-Term Retrieval Goals

Future retrieval capabilities:

- cross-document memory
- startup relationship graph
- investment history retrieval
- fraud pattern similarity matching

````

---

# `/specs/observability.md`

```md
# Observability Specification

# Overview

Observability is mandatory.

Without observability:

- debugging becomes impossible
- hallucinations become invisible
- agent loops become opaque

---

# Logging Requirements

The system MUST log:

- prompts
- model responses
- tool calls
- retries
- failures
- latency
- token usage
- confidence scores

---

# Prompt Tracing

Every prompt execution should include:

```json
{
  "agent": "researcher",
  "prompt_version": "v1.2",
  "latency_ms": 2840,
  "tokens_input": 1820,
  "tokens_output": 640
}
````

---

# Tool Visibility

Every tool call should log:

- tool name
- arguments
- response time
- success/failure

---

# Retry Visibility

The system should track:

- why retries occurred
- retry counts
- degraded responses

---

# Recommended Tools

| Tool          | Purpose             |
| ------------- | ------------------- |
| LangSmith     | Agent tracing       |
| Helicone      | LLM analytics       |
| OpenTelemetry | Distributed tracing |

---

# Error Categories

## Retrieval Failure

Example:

- search API timeout
- vector DB unavailable

---

## Reasoning Failure

Example:

- malformed JSON
- hallucinated evidence
- invalid confidence score

---

## Orchestration Failure

Example:

- graph deadlock
- infinite loops
- retry exhaustion

---

# Debugging Philosophy

Logs should explain:

- what the agent believed
- why it used a tool
- what evidence changed its decision

This is critical for demonstrating true agentic behavior.

````

---

# `/specs/evaluation.md`

```md
# Evaluation Specification

# Overview

Evaluation determines whether Veritas actually works.

A demo without evaluation is not trustworthy.

---

# Benchmark Dataset

Create synthetic startup decks containing:

- inflated TAM
- fake traction
- unrealistic growth
- fabricated partnerships
- inconsistent metrics

---

# Evaluation Goals

Measure:

- claim extraction quality
- contradiction detection accuracy
- hallucination rate
- retrieval precision
- evidence quality

---

# Core Metrics

| Metric | Goal |
|---|---|
| Claim Extraction Accuracy | >90% |
| Contradiction Detection | >80% |
| Hallucination Rate | <5% |
| Retrieval Relevance | High |
| Average Runtime | <20s |

---

# Human Review

Human reviewers should validate:

- evidence quality
- contradiction correctness
- investment memo usefulness

---

# Failure Cases

Track:

- hallucinated claims
- false contradictions
- missing evidence
- weak reasoning

---

# Long-Term Evaluation Goals

Future evaluation:

- adversarial testing
- multi-agent disagreement scoring
- confidence calibration
- reasoning consistency
````

---

# `/specs/api.md`

````md
# API Specification

# Overview

FastAPI powers the Veritas backend.

---

# Authentication

Initial MVP:

- local development only
- no authentication

Future:

- JWT auth
- role-based access
- organization support

---

# Endpoints

## Upload PDF

```http
POST /upload
```
````

Uploads:

- pitch deck
- metadata

Returns:

```json
{
  "document_id": "deck_001"
}
```

---

## Start Analysis

```http
POST /analyze/{document_id}
```

Triggers:

- extraction
- research
- analysis pipeline

---

## Get Report

```http
GET /report/{document_id}
```

Returns:

- final report
- evidence
- contradictions

---

## Get Logs

```http
GET /logs/{document_id}
```

Returns:

- agent traces
- tool calls
- prompt history

---

# Async Processing

Analysis jobs should run asynchronously.

Reasons:

- long-running workflows
- multiple tool calls
- retries
- external latency

---

# Future Endpoints

Potential future APIs:

- portfolio analysis
- batch uploads
- startup comparison
- live monitoring
- webhook integrations

```

```
