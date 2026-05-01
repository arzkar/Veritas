# Veritas Infrastructure Plan: Persistent Data & Multi-Agent State Management

## 1. Overview
To evolve Veritas from a prototype into a professional investigative terminal, we are transitioning from in-memory storage to a persistent, containerized infrastructure. This ensures that every pitch deck investigation, agent audit log, and credibility verdict is stored permanently and is fully auditable after restarts.

## 2. Infrastructure Components

### 2.1 Containerized PostgreSQL
- **Role:** Centralized repository for structured investigative metadata.
- **Why Postgres:** Superior handling of concurrent agent writes and advanced `JSONB` support for storing semi-structured agent reasoning traces.
- **Deployment:** Orchestrated via `docker-compose.yml`.

### 2.2 Persistent Storage Volume
- **Role:** Durable storage for original source material (PDF pitch decks).
- **Structure:** Files will be organized hierarchically by `job_id`.
  - Path: `/data/investigations/{job_id}/source.pdf`
- **Mapping:** The Docker Compose setup will define a named volume (`veritas_vault`) to ensure deck data persists independently of container lifecycles.

### 2.3 High-Fidelity PDF Processing (Docling)
- **Role:** Replaces standard PDF parsing with layout-aware, semantic extraction.
- **Docker Integration:** Docling will run as a dependency within the Backend container.
- **Model Volume:** A dedicated volume (`docling_models`) will be mapped to `/root/.cache/docling` (or equivalent) to persist ML weights and layout-analysis models, preventing expensive re-downloads on every `docker-compose up`.

### 2.4 Resumable Saga Manager (Persistence)
...

### 2.5 Data Governance: Hard Delete Lifecycle
- **Feature:** Ability to completely remove an investigation and its associated artifacts.
- **Workflow:**
  1. User triggers "Delete" in UI.
  2. Backend removes all related records from `agent_audit_logs`, `investigative_claims`, `investigative_slides`, and `investigation_jobs`.
  3. File system service deletes the entire directory associated with the `job_id` from the persistent volume.
- **Outcome:** Clean environment management and data privacy.

---

## 3. Resumption Granularity Matrix
...
| Phase | Scope of Checkpoint | Resumption Logic |
| :--- | :--- | :--- |
| **Ingestion** | Individual Slide | Skips already parsed slides in `investigative_slides`. Starts from first `pending` index. |
| **Extraction** | Full Batch | Re-runs LLM extraction on existing Markdown content if `CLAIMS_READY` is false. |
| **Research** | Individual Claim | Spawns parallel workers only for claims where `belief_state == 'unverified'`. |
| **Analysis** | Individual Claim | Skips claims already marked as `analyzed` or `contradicted`. |
| **Synthesis** | Full Investigation | Re-runs final summary if `status != 'completed'`. |

---

## 4. Data Schema Design

### 4.1 `investigation_jobs` Table
- `id`: UUID (Primary Key)
- `company_name`: String
- `document_path`: String
- `status`: Enum (pending, ingesting, researching, analyzing, synthesizing, completed, failed)
- `current_slide_index`: Integer
- `global_credibility_score`: Float
- `red_flag_count`: Integer
- `synthesis_report`: JSONB
- `created_at`: Timestamp

### 4.2 `investigative_slides` Table
- `id`: UUID
- `job_id`: UUID (Foreign Key)
- `slide_index`: Integer
- `status`: Enum (pending, processed)
- `markdown_content`: Text (Docling output)

### 4.3 `investigative_claims` Table
- `id`: UUID
- `job_id`: UUID (Foreign Key)
- `statement`: Text
- `category`: String
- `importance`: Float
- `belief_state`: Enum (supported, contradicted, absent, ambiguous, unverified)
- `credibility_score`: Float
- `slide_index`: Integer
- `analyst_summary`: Text
- `skeptic_summary`: Text
- `audit_metadata`: JSONB

---

## 5. Implementation Strategy

### 5.1 Phase A: Infrastructure Initialization
1. Create `docker-compose.yml` with **Postgres** and persistent volumes (`veritas_vault`, `docling_models`).
2. Update `.env` with Postgres credentials and TAVILY_API_KEY.

### 5.2 Phase B: Data Access Layer
1. Implement `app/core/database.py` using **SQLAlchemy** (Asynchronous).
2. Define declarative models for Jobs, Slides, Claims, and AuditLogs.

### 5.3 Phase C: Backend Refactor & Docling
1. Integrate **Docling** into `app/services/pdf_parser.py`.
2. Update `app/services/ingestion.py` to use slide-by-slide checkpointing.
3. Update `app/api/routes.py` to utilize Postgres for history and state retrieval.

### 5.4 Phase D: Startup Recovery
1. Add a "Recovery Hook" that scans for non-completed jobs on backend startup and re-triggers them.
2. Refactor LangGraph nodes to connect to the Postgres Checkpointer.
