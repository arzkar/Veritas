# Veritas Tech Stack Specification

# Overview

Veritas is built as a modern Python-first AI agent system.

The stack prioritizes:

- rapid iteration
- observability
- structured outputs
- agent orchestration
- async workflows
- low infrastructure complexity

---

# Core Philosophy

Avoid premature complexity.

Initial architecture should remain:

- monolithic
- async-first
- local-development friendly
- containerized
- modular

The goal is learning and iteration speed.

---

# Backend Stack

| Purpose               | Technology        |
| --------------------- | ----------------- |
| Main Language         | Python            |
| API Framework         | FastAPI           |
| Data Validation       | Pydantic          |
| Async Runtime         | asyncio           |
| Dependency Management | uv / poetry       |
| Environment Config    | pydantic-settings |

---

# Why Python

Python dominates the AI ecosystem.

Critical libraries:

- LangGraph
- LangChain
- LlamaIndex
- sentence-transformers
- FAISS
- OpenAI SDK
- Anthropic SDK
- HuggingFace

The ecosystem maturity is significantly better than alternatives.

---

# FastAPI

## Responsibilities

FastAPI handles:

- PDF uploads
- orchestration triggers
- report retrieval
- async background jobs
- logs and traces

---

## Why FastAPI

Reasons:

- async-native
- modern typing support
- OpenAPI generation
- excellent performance
- integrates perfectly with Pydantic

---

# Agent Orchestration

# Recommended Choice

## LangGraph

Veritas is fundamentally:

```text
A graph orchestration system.
```

not a chatbot.

---

# Why LangGraph

LangGraph supports:

- stateful workflows
- retries
- branching logic
- reflection loops
- multi-agent coordination
- tool routing
- persistent execution state

---

# Alternative Options

| Framework  | Usage                           |
| ---------- | ------------------------------- |
| LangChain  | Basic chaining                  |
| PydanticAI | Structured reasoning            |
| CrewAI     | Simpler multi-agent experiments |

LangGraph remains the preferred architecture.

---

# Structured Outputs

# Pydantic

All agents MUST return typed schemas.

Example:

```python
class Claim(BaseModel):
    claim_id: str
    category: str
    statement: str
    confidence: float
```

---

# Why Structured Outputs Matter

Benefits:

- reliable orchestration
- easier debugging
- safer agent communication
- validation guarantees
- better observability

Avoid freeform agent outputs.

---

# Retrieval Stack

| Purpose         | Technology            |
| --------------- | --------------------- |
| Vector Database | FAISS                 |
| Embeddings      | sentence-transformers |
| Embedding Model | all-MiniLM-L6-v2      |

---

# Why FAISS

Advantages:

- free
- local
- fast
- ideal for experimentation
- no cloud dependency

Future migrations may include:

- Pinecone
- Weaviate
- Qdrant

---

# Embedding Strategy

## Initial Model

```text
all-MiniLM-L6-v2
```

Reasons:

- lightweight
- fast
- good semantic quality
- CPU-friendly
- zero API cost

---

# LLM Stack

| Purpose                       | Model         |
| ----------------------------- | ------------- |
| Cheap orchestration/debugging | GPT-4.1-mini  |
| Heavy reasoning               | Claude Sonnet |
| Local experimentation         | Ollama models |

---

# Model Routing Strategy

## Small Models

Use for:

- extraction
- formatting
- retries
- cheap intermediate steps

---

## Large Models

Use for:

- contradiction analysis
- deep reasoning
- report generation
- adversarial evaluation

---

# Search & External Intelligence

| Purpose              | Tool                |
| -------------------- | ------------------- |
| AI Search            | Tavily              |
| Google Search API    | Serper              |
| Developer Activity   | GitHub API          |
| Startup Intelligence | Crunchbase (future) |

---

# Search Philosophy

Agents should:

- actively retrieve evidence
- compare multiple sources
- validate market claims
- avoid single-source trust

This is core to Veritas.

---

# Observability Stack

| Purpose             | Tool          |
| ------------------- | ------------- |
| Prompt Tracing      | LangSmith     |
| LLM Analytics       | Helicone      |
| Distributed Tracing | OpenTelemetry |

---

# Why Observability Matters

Without observability:

- hallucinations become invisible
- debugging becomes painful
- tool failures become hidden
- agent reasoning becomes opaque

Observability is NOT optional.

---

# Frontend Stack

| Purpose            | Technology  |
| ------------------ | ----------- |
| Frontend Framework | Next.js     |
| Styling            | TailwindCSS |
| Components         | shadcn/ui   |

---

# Frontend Responsibilities

Frontend should support:

- PDF uploads
- evidence visualization
- contradiction dashboards
- agent traces
- final report viewing

Avoid overengineering the frontend initially.

---

# Workflow Automation

## n8n

Use Cases:

- integrations
- webhook automation
- visual workflows
- demos
- scheduled jobs

---

# Important Architecture Note

n8n should NOT contain core reasoning logic.

Core orchestration belongs in:

- LangGraph
- backend services

n8n is supplementary.

---

# Infrastructure

| Purpose                | Tool           |
| ---------------------- | -------------- |
| Containerization       | Docker         |
| CI/CD                  | GitHub Actions |
| Environment Management | .env           |

---

# Initial Deployment Strategy

Start simple.

Recommended:

- local Docker deployment
- single backend service
- single vector DB
- no Kubernetes
- no microservices

Premature infra complexity slows iteration.

---

# Async Programming

# Critical Learning Area

Veritas requires strong async programming.

Important concepts:

```python
async/await
asyncio.gather()
```

---

# Why Async Matters

The system performs:

- parallel searches
- concurrent agent execution
- multiple API calls
- retries
- streaming operations

Async execution significantly improves latency.

---

# Suggested Repository Structure

```text
veritas/
│
├── app/
│   ├── api/
│   ├── agents/
│   ├── orchestration/
│   ├── retrieval/
│   ├── tools/
│   ├── schemas/
│   ├── services/
│   ├── evaluation/
│   └── core/
│
├── frontend/
├── specs/
├── tests/
├── docker/
└── scripts/
```

---

# Learning Priorities

## Phase 1

Learn:

- FastAPI
- Pydantic
- async Python

---

## Phase 2

Learn:

- LangGraph
- tool calling
- structured outputs

---

## Phase 3

Learn:

- vector databases
- embeddings
- retrieval systems

---

## Phase 4

Learn:

- multi-agent orchestration
- reflection loops
- observability
- evaluation

---

# Final Stack Summary

## Backend

- Python
- FastAPI
- LangGraph
- Pydantic

---

## AI Layer

- OpenAI
- Claude
- sentence-transformers

---

## Retrieval

- FAISS
- Tavily
- Serper

---

## Frontend

- Next.js
- TailwindCSS
- shadcn/ui

---

## Infrastructure

- Docker
- GitHub Actions
- uv

---

# Final Philosophy

Veritas should optimize for:

- learning velocity
- experimentation
- reasoning visibility
- orchestration quality
- observability

NOT premature scale.

The project should feel like:

```text
A real AI systems engineering platform.
```
