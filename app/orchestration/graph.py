from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from app.schemas.epistemic import (
    GlobalInvestigationState, 
    Claim, 
    Evidence,
    EpistemicStatus, 
    WorkflowStatus,
    AuditLog
)
from app.core.database import async_session, AuditLogModel, ClaimModel, JobModel
from app.agents.researcher import ResearchAgent
from app.agents.analyst import AnalystAgent
from app.agents.skeptic import SkepticAgent
from app.agents.synthesis import SynthesisAgent
from app.core.belief_engine import BeliefEngine
import logging
import asyncio
import uuid

logger = logging.getLogger(__name__)

# --- Concurrency Control ---
# Limit the number of parallel agent/search tasks to prevent local LLM overload
THROTTLE = asyncio.Semaphore(3)

class GraphState(TypedDict):
    state: GlobalInvestigationState
    evidence_cache: Dict[str, List[Evidence]] # claim_id -> List[Evidence]

class VeritasGraph:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.analyst = AnalystAgent()
        self.skeptic = SkepticAgent()
        self.synthesis = SynthesisAgent()
        self.belief_engine = BeliefEngine()

    async def _add_audit_log(self, job_id: str, agent: str, event: str, msg: str, metadata: Any = None):
        """
        Helper to persist audit logs to Postgres.
        """
        async with async_session() as session:
            db_log = AuditLogModel(
                job_id=uuid.UUID(job_id),
                agent_name=agent,
                event_type=event,
                message=msg,
                metadata_json=metadata
            )
            session.add(db_log)
            await session.commit()

    async def research_node(self, graph_state: GraphState):
        state = graph_state["state"]
        evidence_cache = graph_state.get("evidence_cache", {})
        
        await self._add_audit_log(state.document_id, "Orchestrator", "info", f"Spawning throttled research threads for {len(state.claims)} claims.")
        
        tasks = []
        for claim in state.claims.values():
            if claim.workflow == WorkflowStatus.PENDING:
                tasks.append(self._throttled_research(state, claim, evidence_cache))
        
        if tasks:
            await asyncio.gather(*tasks)
            
        return {"state": state, "evidence_cache": evidence_cache}

    async def _throttled_research(self, state: GlobalInvestigationState, claim: Claim, cache: Dict[str, List[Evidence]]):
        async with THROTTLE:
            await self._add_audit_log(state.document_id, "Researcher", "info", f"Researching claim: '{claim.statement[:60]}...'", {"claim_id": claim.id})
            
            claim.workflow = WorkflowStatus.RESEARCHING
            evidence = await self.researcher.research_claim(claim, state.company_name)
            claim.evidence_ids = [ev.id for ev in evidence]
            cache[claim.id] = evidence 
            
            await self._add_audit_log(state.document_id, "Researcher", "completion", f"Retrieved {len(evidence)} evidence anchors.", {"claim_id": claim.id})
            
            claim.belief = EpistemicStatus.RESEARCHED
            claim.workflow = WorkflowStatus.ANALYZING

    async def analysis_node(self, graph_state: GraphState):
        state = graph_state["state"]
        evidence_cache = graph_state.get("evidence_cache", {})
        
        await self._add_audit_log(state.document_id, "Orchestrator", "info", "Entering forensic analysis and adversarial review phase.")
        
        tasks = []
        for claim in state.claims.values():
            if claim.belief == EpistemicStatus.RESEARCHED:
                evidence = evidence_cache.get(claim.id, [])
                tasks.append(self._throttled_analysis(state, claim, evidence))
                
        if tasks:
            await asyncio.gather(*tasks)
            
        self.belief_engine.update_global_score(state)
        return {"state": state, "evidence_cache": evidence_cache}

    async def _throttled_analysis(self, state: GlobalInvestigationState, claim: Claim, evidence: List[Evidence]):
        async with THROTTLE:
            await self._add_audit_log(state.document_id, "Analyst", "info", "Comparing evidence against claim metric.", {"claim_id": claim.id})
            
            status, credibility, confidence = await self.analyst.analyze_claim(claim, evidence) 
            claim.belief = status
            claim.credibility_score = credibility
            claim.confidence = confidence
            
            if status == EpistemicStatus.CONTRADICTED:
                await self._add_audit_log(state.document_id, "Analyst", "contradiction", "Contradiction discovered!", {"claim_id": claim.id, "summary": claim.analyst_summary})
            
            if claim.importance > 0.7:
                await self._add_audit_log(state.document_id, "Skeptic", "skepticism", "Running adversarial review.", {"claim_id": claim.id})
                skeptic_status, skeptic_score = await self.skeptic.review_claim(claim, evidence)
                
                if skeptic_status == EpistemicStatus.SUSPICIOUSLY_ABSENT:
                    await self._add_audit_log(state.document_id, "Skeptic", "contradiction", "Suspicious Absence detected!", {"claim_id": claim.id})
                claim.belief = skeptic_status
                
            claim.workflow = WorkflowStatus.COMPLETED
            
            # Sync claim update back to DB for Phase D resumption
            async with async_session() as session:
                await session.execute(
                    update(ClaimModel).where(ClaimModel.id == uuid.UUID(claim.id)).values(
                        belief_state=claim.belief,
                        credibility_score=claim.credibility_score,
                        analyst_summary=claim.analyst_summary,
                        skeptic_summary=claim.skeptic_summary
                    )
                )
                await session.commit()

    async def synthesis_node(self, graph_state: GraphState):
        state = graph_state["state"]
        await self._add_audit_log(state.document_id, "Synthesis", "info", "Finalizing global narrative synthesis.")
        
        result = await self.synthesis.synthesize_investigation(state)
        state.synthesis_report = str(result)
        
        await self._add_audit_log(state.document_id, "Orchestrator", "completion", "Investigation lifecycle complete.")
        return {"state": state}

    def _should_continue(self, graph_state: GraphState):
        state = graph_state["state"]
        for claim in state.claims.values():
            if (claim.belief == EpistemicStatus.AMBIGUOUS and 
                claim.importance > 0.8 and 
                claim.research_iterations < claim.max_research_budget):
                return "research"
        return "synthesize"

    def compile(self):
        workflow = StateGraph(GraphState)
        workflow.add_node("research", self.research_node)
        workflow.add_node("analyze", self.analysis_node)
        workflow.add_node("synthesize", self.synthesis_node)
        workflow.set_entry_point("research")
        workflow.add_edge("research", "analyze")
        workflow.add_conditional_edges("analyze", self._should_continue, {"research": "research", "synthesize": "synthesize"})
        workflow.add_edge("synthesize", END)
        return workflow.compile()
