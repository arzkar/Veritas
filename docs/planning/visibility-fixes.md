# Veritas Planning: Live Visibility & Interactivity Enhancements

## 1. Overview
During the initial end-to-end tests, a "Visibility Lag" was identified where the backend performs significant investigative work (researching 21+ claims), but the UI remains static until the entire processing node completes. Additionally, the extraction of "Hard Claims" sometimes lacks semantic context, and the claim inspection system remains disconnected.

This plan details the enhancements required to make the investigation feel "alive" and interactive.

---

## 2. Real-Time "Live Feed" Log Streaming

### 2.1 The Problem
Currently, `audit_logs` are sent to the UI via `state_update` events, which only fire after a LangGraph node (e.g., `research_node`) finishes. For a large deck, this can lead to 2-3 minutes of a blank "Audit Log" pane.

### 2.2 The Fix: Instant Log Dispatch
- **Backend:** Update the `ConnectionManager` to support a new message type: `audit_log_entry`.
- **Instrumentation:** Inside the `VeritasGraph` helper methods (like `_process_claim_research`), we will call `manager.broadcast` **immediately** after creating an `AuditLog` object.
- **Frontend:** Update the Zustand store and WebSocket hook to append logs to the `auditLogs` array as soon as they arrive, rather than replacing the whole list.

---

## 3. Claim Inspection & Evidence Loading

### 3.1 The Problem
The right-hand panel ("Evidence Explorer") currently shows "Node Offline" because clicking a claim card in the sidebar does not update the `activeClaimId` in the global state.

### 3.2 The Fix: Inter-Panel Selection
- **Store Update:** Add `selectedClaimId: string | null` to the `useInvestigationStore`.
- **UI Interaction:** Add an `onClick` handler to the Claim cards in the left panel to set the `selectedClaimId`.
- **Evidence Hydration:** The right panel will filter the `evidence` store for the `selectedClaimId` and render the retrieved snippets (URLs, titles, authority scores).

---

## 4. Contextual Extraction (Docling Integration)

### 4.1 The Problem
Extracted claims like "$200M" or "10.6M" are semantically "sparse." The current `PyMuPDF` parser returns linear text that breaks the visual relationship between a metric and its label (e.g., "TAM").

### 4.2 The Fix: Docling Markdown Pipeline
- **Replacement:** Replace `PyMuPDF` with **Docling** in `app/services/pdf_parser.py`.
- **Markdown Core:** Use Docling to convert each slide into high-fidelity **Markdown**. Markdown preserves structure (headers, lists, tables) better than raw text.
- **Prompt Refinement:** Update the `ExtractorAgent` system prompt to extract from Markdown. 
- **Requirement:** "Every extracted statement MUST include the primary metric AND its associated noun or context. (e.g., 'Total Addressable Market: $200M' instead of just '$200M')."

---

## 5. Performance: Investigative Throttling (The "Stuck" Fix)

### 5.1 The Problem
When a deck contains many claims (e.g., 20+), the system attempts to research them all simultaneously using `asyncio.gather`. This overwhelms the local Ollama instance, causing massive latency and making the UI appear frozen.

### 5.2 The Fix: Concurrency Semaphore
- **Implementation:** Introduce an `asyncio.Semaphore(limit=3)` in the `VeritasGraph`.
- **Behavior:** This will limit the number of active LLM/Search threads. As one claim finishes, the next one in the queue begins.
- **Outcome:** Predictable performance, steady "Live Feed" updates, and no system-wide hangs.

---

## 6. Technical Implementation Order

1. **Step 1 (Docling):** Integrate Docling and refine the `ExtractorAgent` prompt.
2. **Step 2 (Logs):** Implement `audit_log_entry` broadcasting and **Throttling**.
3. **Step 3 (Interactivity):** Add selection logic and **Delete Functionality**.

---

## 6. Expected Outcome
The user will be able to watch the "Investigation Unfold" line-by-line in the center panel, click on claims as they appear to see evidence flowing in, and read semantically complete claims that represent the pitch deck's narrative accurately.
