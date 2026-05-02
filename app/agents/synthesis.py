from langchain_ollama import OllamaLLM
from app.schemas.epistemic import GlobalInvestigationState, Claim, EpistemicStatus
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class SynthesisAgent:
    """
    Agent responsible for holistic narrative coherence and global risk assessment.
    The 'Partner' level reviewer who looks at the big picture.
    """
    
    def __init__(self, model_name: str = "qwen3:8b"):
        self.llm = OllamaLLM(model=model_name, temperature=0.2)
        
    def _get_synthesis_prompt(self, company_name: str, sector: str, claims: List[Dict[str, Any]], global_score: float) -> str:
        claims_context = ""
        for i, c in enumerate(claims):
            claims_context += f"CLAIM {i+1} [{c['category']}]: \"{c['statement']}\"\n"
            claims_context += f"  STATUS: {c['belief']}\n"
            claims_context += f"  CREDIBILITY: {c['credibility_score']}\n"
            if c.get('analyst_summary'):
                claims_context += f"  ANALYSIS: {c['analyst_summary']}\n"
            if c.get('skeptic_summary'):
                claims_context += f"  SKEPTIC NOTES: {c['skeptic_summary']}\n"
            claims_context += "\n"
            
        return f"""You are a Senior Venture Capital Diligence Partner. Your task is to provide a final synthesis of a startup investigation.

COMPANY: {company_name or 'Unknown'}
SECTOR: {sector or 'Unknown'}
GLOBAL CREDIBILITY SCORE: {global_score}

INVESTIGATION FINDINGS:
{claims_context}

SYNTHESIS GOALS:
1. Narrative Coherence: Does the story make sense globally? (e.g., massive growth vs small team).
2. Risk Identification: What are the primary 'Red Flags' or 'Deal Breakers'?
3. Strategic Tension: Are there contradictory business model claims?
4. Final Verdict: Provide a nuanced recommendation (Proceed, Caution, or Reject).

Return a JSON object. Do not include any preamble.
STRUCTURE:
{{
    "executive_summary": "High-level 2-3 sentence summary",
    "narrative_coherence_analysis": "Analysis of how well the claims fit together",
    "top_red_flags": ["List", "of", "critical", "concerns"],
    "investment_recommendation": "One of: PROCEED, CAUTION, REJECT",
    "recommendation_reasoning": "Detailed justification for the verdict"
}}"""

    async def synthesize_investigation(self, state: GlobalInvestigationState) -> Dict[str, Any]:
        """
        Runs the final global analysis on the investigation state.
        """
        claims_data = []
        for claim in state.claims.values():
            claims_data.append({
                "statement": claim.statement,
                "category": claim.category,
                "belief": claim.belief,
                "credibility_score": claim.credibility_score,
                "analyst_summary": claim.analyst_summary,
                "skeptic_summary": claim.skeptic_summary
            })
            
        prompt = self._get_synthesis_prompt(
            state.company_name, 
            state.target_sector, 
            claims_data, 
            state.global_credibility_score
        )
        
        try:
            response = await self.llm.ainvoke(prompt)
            raw_json = response.strip().strip("```json").strip("```").strip()
            return json.loads(raw_json)
        except Exception as e:
            logger.error(f"Synthesis failed: {str(e)}")
            return {
                "executive_summary": "Manual review required due to synthesis failure.",
                "investment_recommendation": "CAUTION"
            }
