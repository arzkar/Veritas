# Veritas: Autonomous AI Due Diligence Terminal

Veritas is a local-first, multi-agent AI system designed to perform adversarial due diligence on startup pitch decks. Unlike standard chatbots, Veritas operates as an **Investigative Operating System**—treating startup claims as hypotheses to be verified against external reality.

## 🚀 Key Features

- **Zero-Trust Claim Extraction:** Automatically identifies "Hard Claims" (revenue, growth, partners) while filtering out marketing fluff.
- **Adversarial Research:** Dispatches agents to find evidence that _contradicts_ startup claims using Tavily & Serper.
- **The Skeptic Agent:** Models "expected visibility" to detect "the dog that didn't bark"—identifying when evidence is suspiciously absent.
- **Bayesian Credibility Engine:** Mathematically propagates trust and decay throughout the company narrative.
- **Investigative Terminal:** A multi-panel Dashboard built with Next.js for real-time trace inspection and source-grounded reasoning.

---

## 🛠 Tech Stack

- **Reasoning:** Ollama (`qwen2.5:8b`)
- **Orchestration:** LangGraph (Stateful, cyclical multi-agent workflows)
- **Backend:** FastAPI (Async IO & WebSockets)
- **Frontend:** Next.js 14, TailwindCSS, shadcn/ui, Zustand
- **Retrieval:** FAISS (Local session-based vector storage)
- **Search:** Tavily AI Search

---

## 🏁 Getting Started

### 1. Prerequisites

- **Python 3.12+** (via `pyenv`)
- **Node.js 18+**
- **Ollama** installed and running

### 2. Setup Models

Pull the required local models for reasoning and embeddings:

```bash
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
TAVILY_API_KEY=your_api_key_here
```

### 4. Installation

```bash
# Activate your environment
pyenv activate veritas

# Install Python dependencies
pip install -r requirements.txt

# Install Frontend dependencies
cd frontend
npm install
```

---

## 🏃 Running the System

### Step 1: Start the Backend

```bash
# In the root directory
python -m app.main
```

_The API will be available at `http://localhost:8000`_

### Step 2: Start the Frontend

```bash
# In a new terminal
cd frontend
npm run dev
```

_The Terminal UI will be available at `http://localhost:3000`_

---

## 📂 Project Structure

```text
├── app/
│   ├── agents/          # Extractor, Researcher, Analyst, Skeptic, Synthesis
│   ├── api/             # FastAPI routes & WebSocket manager
│   ├── core/            # Belief Engine & Bayesian logic
│   ├── orchestration/   # LangGraph workflow definitions
│   ├── retrieval/       # FAISS & local vector store service
│   ├── schemas/         # Pydantic V2 Epistemic models
│   └── services/        # PDF Parsing & Ingestion logic
├── docs/                # Technical & UI/UX Specifications
├── frontend/            # Next.js 14 Investigative Terminal
└── scripts/             # Standalone test scripts for agents
```

---

## ⚖️ Epistemic Philosophy

Veritas is built on **Institutional Skepticism**.

- **Supported:** Evidence corroborates the claim.
- **Contradicted:** Reality conflicts with the narrative.
- **Suspiciously Absent:** A high-impact claim has zero external footprint.
- **Ambiguous:** Conflicting or low-quality data.

---

## 📜 Documentation

For deep-dives into the architecture, see:

- `docs/technical-specification.md`
- `docs/ui-ux-specification.md`
- `TASKS.md`

---

_Built for the future of rigorous financial intelligence._
