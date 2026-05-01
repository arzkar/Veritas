from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
import uuid

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    EXTRACTING = "extracting"
    RESEARCHING = "researching"
    ANALYZING = "analyzing"
    SKEPTIC_REVIEW = "skeptic_review"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    STALLED = "stalled"
    FAILED = "failed"

class EpistemicStatus(str, Enum):
    UNVERIFIED = "unverified"
    RESEARCH_PENDING = "research_pending"
    RESEARCHED = "researched"
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    SUSPICIOUSLY_ABSENT = "absent"
    AMBIGUOUS = "ambiguous"
    DEBUNKED = "debunked"

class ClaimCategory(str, Enum):
    TRACTION = "traction" # Generic fallback
    REVENUE = "revenue"   # Generic fallback
    TEAM = "team"         # Generic fallback
    MARKET = "market"     # Generic fallback
    FINANCIAL_REVENUE = "financial_revenue"
    FINANCIAL_FUNDING = "financial_funding"
    TRACTION_USERS = "traction_users"
    TRACTION_GROWTH = "traction_growth"
    TEAM_EXPERIENCE = "team_experience"
    TEAM_EDUCATION = "team_education"
    MARKET_SIZE = "market_size"
    MARKET_SHARE = "market_share"
    UNIT_ECONOMICS = "unit_economics"
    TECHNOLOGY_PROPRIETARY = "technology_proprietary"
    TECHNOLOGY_INFRA = "technology_infra"
    PARTNERSHIPS = "partnerships"
    COMPETITION = "competition"
    LEGAL_COMPLIANCE = "legal_compliance"

class ConfidenceMetrics(BaseModel):
    extraction: float = Field(0.5, ge=0, le=1.0, description="Confidence in the PDF parsing/OCR accuracy.")
    retrieval: float = Field(0.0, ge=0, le=1.0, description="Quality/Relevance of the search results found.")
    analysis: float = Field(0.0, ge=0, le=1.0, description="Confidence in the Analyst's logic matching.")
    
    @property
    def aggregate(self) -> float:
        # Weighted average prioritization
        # Research and Analysis are critical for truth-determination
        weights = {"extraction": 0.2, "retrieval": 0.4, "analysis": 0.4}
        return (self.extraction * weights["extraction"]) + \
               (self.retrieval * weights["retrieval"]) + \
               (self.analysis * weights["analysis"])

class Evidence(BaseModel):
    id: str = Field(..., description="Unique hash-based identifier for the evidence snippet.")
    source_type: str = Field(..., description="e.g., 'web_search', 'github_api', 'benchmark_db', 'sec_filing'")
    url: Optional[HttpUrl] = None
    title: Optional[str] = None
    content_snippet: str
    
    # Uncertainty & Trust Metrics
    source_authority: float = Field(0.5, ge=0, le=1.0, description="Weighted trust in the domain/source.")
    recency_score: float = Field(1.0, ge=0, le=1.0, description="Time-decay factor for relevance.")
    relevance_to_claim: float = Field(1.0, ge=0, le=1.0, description="Semantic alignment with the specific claim.")
    
    # Impact Analysis
    supports_claim: bool = Field(..., description="Directional result: Does this evidence confirm or deny?")
    sentiment_score: float = Field(0.0, ge=-1.0, le=1.0, description="Intensity of support/contradiction.")
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)

class Claim(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    statement: str = Field(..., description="The literal declarative statement from the pitch deck.")
    category: ClaimCategory = Field(..., description="Categorical classification for specialized routing.")
    importance: float = Field(0.5, ge=0, le=1.0, description="Significance to the overall investment decision.")
    
    # Epistemic & Operational State
    workflow: WorkflowStatus = WorkflowStatus.PENDING
    belief: EpistemicStatus = EpistemicStatus.UNVERIFIED
    confidence: ConfidenceMetrics = Field(default_factory=ConfidenceMetrics)
    
    # Provenance
    primary_slide: int = Field(..., description="The main slide number where this claim originated.")
    related_slides: List[int] = Field(default_factory=list, description="Other slides providing context.")
    extraction_method: str = Field(..., description="Method used: 'text', 'ocr', or 'multimodal'.")
    
    # Investigation Results
    credibility_score: float = Field(0.5, ge=0, le=1.0, description="Probability of claim truthfulness.")
    evidence_ids: List[str] = Field(default_factory=list, description="References to Evidence objects.")
    research_iterations: int = 0
    max_research_budget: int = 3
    
    # Reasoning Trace
    skeptic_summary: Optional[str] = None
    analyst_summary: Optional[str] = None
    red_flag_severity: float = Field(0.0, ge=0, le=1.0)

class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_name: str # "Extractor", "Researcher", "Analyst", "Skeptic", "Synthesis", "Orchestrator"
    event_type: str # "info", "warning", "skepticism", "contradiction", "completion"
    message: str
    metadata: Optional[Dict[str, Any]] = None

class GlobalInvestigationState(BaseModel):
    document_id: str
    company_name: Optional[str] = None
    target_sector: Optional[str] = None
    
    # The Global Belief Model
    global_credibility_score: float = 1.0  # Decays as red flags emerge
    red_flag_count: int = 0
    
    # Active Investigation Threads
    claims: Dict[str, Claim] = Field(default_factory=dict)
    audit_logs: List[AuditLog] = Field(default_factory=list)
    
    # Resource Management
    total_token_usage: int = 0
    investigation_depth: int = 0
    max_depth: int = 5
    
    # Final Output
    synthesis_report: Optional[str] = None
