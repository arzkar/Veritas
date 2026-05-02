from langchain_ollama import OllamaLLM
from app.schemas.epistemic import Claim, Evidence, EpistemicStatus
from typing import List, Dict, Any, Tuple
import json
import logging

logger = logging.getLogger(__name__)

class SkepticAgent:
    """
    Adversarial agent responsible for detecting "Suspicious Absence" and impossible claims.
    Acts as the 'Devil's Advocate' for the startup narrative.
    """
    
    def __init__(self, model_name: str = "qwen3:8b"):
        self.llm = OllamaLLM(model=model_name, temperature=0.3) # Slightly higher temperature for 'adversarial creativity'
        
    def _get_skeptic_prompt(self, claim: str, category: str, evidence_count: int) -> str:
        return f"""You are an Adversarial Due Diligence Investigator. Your job is to find reasons NOT to believe a startup claim.
        
CLAIM: "{claim}"
CATEGORY: {category}
EVIDENCE PIECES FOUND: {evidence_count}

CONCEPT: "Expected Visibility Modeling"
If this claim were true, what evidence SHOULD exist in the public domain (GitHub, News, LinkedIn, Patents, Industry Reports)?
If the evidence count is low (0-2) for a high-impact claim, this is highly suspicious.

REASONING GUIDELINES:
1. "The Ghost Customer": Claiming massive partners but zero public footprint.
2. "The Vaporware Tech": Proprietary breakthrough with 0 patents or GitHub activity.
3. "The Inflated TAM": Claiming a market larger than realistic sector benchmarks.
4. "The Paper Team": High-profile advisors with no verifiable connection.

Return a JSON object. Do not include any preamble.
STRUCTURE:
{{
    "skepticism_score": 0.0 to 1.0 (1.0 = highly skeptical/suspicious),
    "is_suspiciously_absent": true/false,
    "reasoning": "Detailed explanation of why this claim seems impossible or unverified",
    "missing_evidence_types": ["List", "of", "missing", "anchors"],
    "adversarial_status": "One of: absent, ambiguous, unverified"
}}"""

    async def review_claim(self, claim: Claim, evidence: List[Evidence]) -> Tuple[EpistemicStatus, float]:
        """
        Reviews a claim for suspicious absence of evidence.
        """
        prompt = self._get_skeptic_prompt(claim.statement, claim.category, len(evidence))
        
        try:
            response = await self.llm.ainvoke(prompt)
            raw_json = response.strip().strip("```json").strip("```").strip()
            result = json.loads(raw_json)
            
            skeptic_score = float(result.get("skepticism_score", 0.0))
            claim.skeptic_summary = result.get("reasoning")
            
            # Update status if suspiciously absent
            new_status = claim.belief
            if result.get("is_suspiciously_absent") and len(evidence) < 2:
                new_status = EpistemicStatus.SUSPICIOUSLY_ABSENT
                
            return new_status, skeptic_score
            
        except Exception as e:
            logger.error(f"Skeptic review failed for claim {claim.id}: {str(e)}")
            return claim.belief, 0.5
