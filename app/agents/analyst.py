from langchain_ollama import OllamaLLM
from app.schemas.epistemic import Claim, Evidence, EpistemicStatus, ConfidenceMetrics
from typing import List, Dict, Any, Tuple
import json
import logging

logger = logging.getLogger(__name__)

class AnalystAgent:
    """
    Agent responsible for comparing startup claims against retrieved evidence.
    Detects support, contradictions, and sentiment deltas.
    """
    
    def __init__(self, model_name: str = "qwen3:8b"):
        self.llm = OllamaLLM(model=model_name, temperature=0.1)
        
    def _get_analysis_prompt(self, claim: str, evidence: List[Dict[str, Any]]) -> str:
        evidence_context = ""
        for i, ev in enumerate(evidence):
            evidence_context += f"EVIDENCE {i+1} (Source: {ev.get('title', 'Unknown')}):\n{ev.get('content_snippet', '')}\n\n"
            
        return f"""You are a Forensic Financial Auditor. Your task is to compare a startup's CLAIM against external EVIDENCE.

CLAIM: "{claim}"

{evidence_context}

ANALYSIS GUIDELINES:
1. Identify the 'Core Metric' or 'Core Fact' in the claim (e.g., "$10M ARR", "40% market share").
2. Identify the corresponding data points in the evidence.
3. Determine the 'Epistemic Delta': how far is the claim from reality?
4. Assign a belief status:
   - SUPPORTED: Evidence strongly corroborates the claim.
   - CONTRADICTED: Evidence directly conflicts with or significantly scales down the claim.
   - AMBIGUOUS: Evidence is conflicting, outdated, or doesn't directly address the metric.
   - DEBUNKED: Irrefutable evidence that the claim is false.

Return a JSON object. Do not include any preamble.
STRUCTURE:
{{
    "status": "One of: supported, contradicted, ambiguous, debunked",
    "credibility_score": 0.0 to 1.0 (1.0 = highly believable),
    "sentiment_score": -1.0 to 1.0 (-1.0 = strong contradiction, 1.0 = strong support),
    "analysis_summary": "Short explanation of the finding",
    "key_contradiction": "Description of the specific conflict found, if any",
    "evidence_confidence": 0.0 to 1.0 (How reliable is this evidence set?)
}}"""

    async def analyze_claim(self, claim: Claim, evidence: List[Evidence]) -> Tuple[EpistemicStatus, float, ConfidenceMetrics]:
        """
        Performs comparative analysis between a claim and a list of evidence.
        """
        if not evidence:
            return EpistemicStatus.UNVERIFIED, 0.5, claim.confidence
            
        # Convert evidence list for prompt
        ev_data = [
            {"title": ev.title, "content_snippet": ev.content_snippet} 
            for ev in evidence
        ]
        
        prompt = self._get_analysis_prompt(claim.statement, ev_data)
        
        try:
            response = await self.llm.ainvoke(prompt)
            raw_json = response.strip().strip("```json").strip("```").strip()
            result = json.loads(raw_json)
            
            # Map status string to Enum
            status_map = {
                "supported": EpistemicStatus.SUPPORTED,
                "contradicted": EpistemicStatus.CONTRADICTED,
                "ambiguous": EpistemicStatus.AMBIGUOUS,
                "debunked": EpistemicStatus.DEBUNKED
            }
            
            new_status = status_map.get(result["status"].lower(), EpistemicStatus.AMBIGUOUS)
            credibility = float(result.get("credibility_score", 0.5))
            
            # Update confidence
            new_confidence = claim.confidence.copy()
            new_confidence.analysis = 0.9
            new_confidence.retrieval = result.get("evidence_confidence", 0.7)
            
            # Record reasoning in claim (caller will update the object)
            claim.analyst_summary = result.get("analysis_summary")
            if new_status == EpistemicStatus.CONTRADICTED:
                claim.red_flag_severity = abs(float(result.get("sentiment_score", 0.0)))
            
            return new_status, credibility, new_confidence
            
        except Exception as e:
            logger.error(f"Analysis failed for claim {claim.id}: {str(e)}")
            return EpistemicStatus.AMBIGUOUS, 0.5, claim.confidence
