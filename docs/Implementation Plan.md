# Veritas — Implementation Plan

## Vision

**Veritas** is an AI-powered autonomous due diligence platform that analyzes startup pitch decks, validates claims using external data sources, detects inconsistencies, and generates structured investment risk reports.

The core idea is:

> “Never trust founder claims blindly.”

Veritas acts like a junior VC analyst team:

- extracting information,
- researching the market,
- validating claims,
- identifying red flags,
- and generating investment memos.

---

# Phase 0 — Goals & Scope

## Initial MVP Goal

Build a working system that can:

1. Upload a startup PDF
2. Extract key claims
3. Search the web for verification
4. Compare external evidence with claims
5. Generate:
   - contradictions
   - risks
   - confidence scores
   - due diligence summary

---

# High-Level Architecture

```text
User Uploads Pitch Deck
           ↓
    PDF Processing Layer
           ↓
     Extractor Agent
           ↓
      Claim Objects
           ↓
     Research Agent
           ↓
 External Search + Vector DB
           ↓
    Analyst Agent
           ↓
 Contradiction + Risk Analysis
           ↓
     Final VC Memo Report
```

---

# Core Tech Stack

| Layer              | Technology              |
| ------------------ | ----------------------- |
| Backend            | Python + FastAPI        |
| Agent Framework    | LangGraph or LangChain  |
| Workflow UI        | n8n                     |
| Vector DB          | FAISS or Chroma         |
| LLM                | GPT-4.1 / Claude Sonnet |
| Search APIs        | Tavily + Serper         |
| Embeddings         | all-MiniLM-L6-v2        |
| Observability      | LangSmith               |
| PDF Parsing        | PyMuPDF / pdfplumber    |
| Structured Outputs | Pydantic                |

---

# Repository Structure

```text
veritas/
│
├── agents/
│   ├── extractor.py
│   ├── researcher.py
│   ├── analyst.py
│   └── skeptic.py
│
├── workflows/
│   ├── langgraph_pipeline.py
│   └── n8n/
│
├── retrieval/
│   ├── vector_store.py
│   ├── embeddings.py
│   └── chunking.py
│
├── tools/
│   ├── tavily_search.py
│   ├── serper_search.py
│   ├── github_lookup.py
│   └── crunchbase_lookup.py
│
├── schemas/
│   ├── claim.py
│   ├── evidence.py
│   └── report.py
│
├── evaluation/
│   ├── benchmark_cases/
│   └── metrics.py
│
├── logs/
│
├── api/
│   └── routes.py
│
├── frontend/
│
└── README.md
```

---

# Phase 1 — PDF Extraction Pipeline

## Objective

Convert startup pitch decks into structured claim data.

---

## Tasks

### 1. PDF Upload Endpoint

Build FastAPI endpoint:

```python
POST /upload
```

Accept:

- PDF file
- metadata

---

### 2. Extract Raw Text

Use:

- PyMuPDF
- pdfplumber

Extract:

- slide text
- headings
- tables
- metrics

---

### 3. Chunking Strategy

Chunk by:

- slide
- section
- semantic meaning

Store metadata:

```json
{
  "slide": 4,
  "type": "market_claim",
  "company": "ExampleAI"
}
```

---

### 4. Embeddings + Vector DB

Use:

- sentence-transformers
- FAISS

Store:

- text chunks
- metadata

---

# Phase 2 — Extractor Agent

## Objective

Convert raw startup deck into structured claims.

---

## Claim Schema

```python
class Claim(BaseModel):
    claim_id: str
    category: str
    statement: str
    source_slide: int
    confidence: float
```

---

## Categories

- Market Share
- Revenue
- User Growth
- Team
- Competitors
- TAM/SAM/SOM
- Product Claims
- AI/Technology Claims
- Partnerships

---

## Prompt Strategy

System Prompt:

```text
You are a forensic startup analyst.

Extract ONLY objective claims.
Ignore marketing language.
Return structured JSON.
```

---

# Phase 3 — Research Agent

## Objective

Verify startup claims using external tools.

---

# Tooling Layer

## Tavily

Use for:

- company search
- market verification
- funding news

---

## Serper

Use for:

- Google search
- indexed competitor discovery

---

## GitHub API

Check:

- repository activity
- contributor count
- commit frequency

---

## Optional Future Tools

- Crunchbase
- Pitchbook
- LinkedIn
- SEC filings
- YC database

---

# Research Workflow

```text
Claim
  ↓
Generate Search Queries
  ↓
Search APIs
  ↓
Collect Evidence
  ↓
Rank Evidence
  ↓
Return Findings
```

---

## Example

### Input Claim

```text
"We hold 40% of the European fintech market."
```

### Generated Queries

```text
Top European fintech companies market share 2026
Largest fintech firms Europe
European fintech market report
```

---

# Evidence Schema

```python
class Evidence(BaseModel):
    source: str
    url: str
    snippet: str
    relevance_score: float
    supports_claim: bool
```

---

# Phase 4 — Analyst Agent

## Objective

Identify contradictions and produce investment insights.

---

# Responsibilities

## Detect:

- exaggerated claims
- impossible metrics
- fake market dominance
- unrealistic growth
- weak traction
- inactive engineering teams
- misleading TAM estimates

---

## Generate

### Risk Report

```json
{
  "risk_level": "HIGH",
  "issues": [
    "Claimed market dominance unsupported",
    "GitHub inactive for 8 months"
  ]
}
```

---

# Phase 5 — Skeptic Agent

## Objective

Actively attempt to disprove startup claims.

This is the adversarial reasoning layer.

---

# Examples

## Questions it asks

- Does this metric make economic sense?
- Is the market actually this large?
- Are competitors already dominant?
- Is this traction fabricated?
- Does employee count match claimed growth?

---

# Why This Matters

This creates:

- deeper reasoning
- conflict analysis
- more realistic due diligence

---

# Phase 6 — Orchestration Layer

## Option A — LangGraph (Recommended)

Why:

- stateful workflows
- retries
- branching
- reflection loops

---

## Example Flow

```text
Extractor
   ↓
Researcher
   ↓
Analyst
   ↓
Skeptic
   ↓
Reflection Loop
   ↓
Final Report
```

---

## Option B — n8n

Use for:

- visual workflows
- API orchestration
- demos
- integrations

---

# Phase 7 — Observability

## CRITICAL

This is what separates serious AI systems from demos.

---

# Log Everything

## Store:

- prompts
- responses
- latency
- token usage
- tool calls
- failures
- retries
- confidence scores

---

# Recommended Tools

| Tool          | Purpose          |
| ------------- | ---------------- |
| LangSmith     | Agent tracing    |
| Helicone      | LLM analytics    |
| OpenTelemetry | Advanced tracing |

---

# Phase 8 — Evaluation Framework

## Objective

Measure whether Veritas actually works.

---

# Create Benchmark Cases

## Examples

### Fake Startup Deck

Contains:

- inflated revenue
- fake competitors
- impossible market size

---

# Metrics

| Metric                    | Goal |
| ------------------------- | ---- |
| Claim Extraction Accuracy | >90% |
| Contradiction Detection   | >80% |
| Hallucination Rate        | <5%  |
| Retrieval Precision       | High |
| Response Latency          | <20s |

---

# Phase 9 — Frontend

## MVP UI

Simple dashboard:

### Features

- Upload PDF
- View extracted claims
- View evidence
- See contradictions
- Download VC memo

---

# Suggested Stack

- Next.js
- Tailwind
- shadcn/ui

---

# Phase 10 — Advanced Features

## Future Ideas

### 1. Multi-document analysis

Compare:

- pitch deck
- founder tweets
- GitHub
- previous funding announcements

---

### 2. Memory System

Remember:

- previous startup analyses
- competitor history
- prior red flags

---

### 3. Investment Scoring

Generate:

- conviction score
- fraud probability
- diligence completeness score

---

### 4. Human-in-the-loop

Allow analysts to:

- approve findings
- override scores
- annotate evidence

---

# Development Roadmap

| Week | Goal                       |
| ---- | -------------------------- |
| 1    | PDF extraction + vector DB |
| 2    | Claim extraction agent     |
| 3    | Tavily/Serper integration  |
| 4    | Research agent             |
| 5    | Analyst agent              |
| 6    | Skeptic agent              |
| 7    | LangGraph orchestration    |
| 8    | Frontend dashboard         |
| 9    | Evaluation framework       |
| 10   | Polish + demo video        |

---

# MVP Deliverable

By the end, Veritas should:

✅ Read startup decks
✅ Extract claims
✅ Search the web autonomously
✅ Verify market statements
✅ Detect contradictions
✅ Generate due diligence reports
✅ Show reasoning traces
✅ Demonstrate agent collaboration

---

# Portfolio Goal

The final demo should emphasize:

- multi-agent orchestration
- autonomous tool use
- reasoning traces
- retrieval pipelines
- observability
- adversarial analysis
- structured outputs

---

# Demo Script Idea

```text
1. Upload startup deck
2. Veritas extracts claims
3. Research agent searches web
4. Skeptic agent disputes findings
5. Analyst produces risk report
6. Dashboard highlights contradictions
```

---

# Final Philosophy

Veritas is NOT:

- a chatbot
- a PDF summarizer
- a generic RAG app

Veritas is:

> an autonomous due diligence analyst system.

That distinction is what makes the project impressive.
