from langchain_ollama import OllamaLLM
from app.schemas.epistemic import Claim, ClaimCategory, ConfidenceMetrics, WorkflowStatus, EpistemicStatus
from typing import List, Dict, Any
import json
import logging
import uuid

logger = logging.getLogger(__name__)

class ExtractorAgent:
    """
    Agent responsible for converting raw slide text into structured, 
    verifiable Claim objects using a local LLM.
    """
    
    def __init__(self, model_name: str = "qwen3:8b"): # Using qwen2.5 as qwen3 is not out yet, usually 2.5 is the latest stable
        self.llm = OllamaLLM(model=model_name, temperature=0.1) # Low temperature for extraction precision
        
    def _get_system_prompt(self) -> str:
        return """You are a Forensic VC Analyst. Your goal is to identify ALL declarative, verifiable "Hard Claims" from the provided startup slide text.

A "Hard Claim" is:
- A specific number (Revenue, Users, Growth %, Employee counts)
- A name (Partners, Investors, Competitors, specific customers)
- A declarative fact (Patented tech, First-mover status, specific degrees/exits)

IGNORE:
- Vision statements ("We want to revolutionize...")
- Marketing adjectives ("Best-in-class," "Industry-leading")
- Mission statements
- Team bios that don't list specific companies/universities

Return a JSON list of objects. Each object MUST strictly follow this structure:
{
    "statement": "The exact literal claim",
    "category": "One of: traction, revenue, team, market_size, unit_economics, technology, partnerships, competition, legal",
    "importance": 0.0 to 1.0 (Financials=1.0, Traction=0.9, Market=0.7, Vision=0.1)
}

If no hard claims are found, return an empty list [].
Do not include any preamble or explanation, only the JSON list."""

    async def extract_claims(self, slide_text: str, slide_index: int) -> List[Claim]:
        """
        Parses slide text into structured Claim objects.
        """
        if not slide_text.strip():
            return []
            
        prompt = f"{self._get_system_prompt()}\n\nSLIDE TEXT:\n{slide_text}"
        
        try:
            response = await self.llm.ainvoke(prompt)
            # Basic cleaning in case of markdown blocks
            raw_json = response.strip().strip("```json").strip("```").strip()
            
            if not raw_json or raw_json == "[]":
                return []
                
            claim_data = json.loads(raw_json)
            
            claims = []
            for data in claim_data:
                # Map string category to Enum
                raw_cat = data.get("category", "traction").lower()
                
                # Dynamic mapping lookup
                category = ClaimCategory.TRACTION
                for member in ClaimCategory:
                    if member.value == raw_cat:
                        category = member
                        break
                
                claim = Claim(
                    id=str(uuid.uuid4()),
                    statement=data["statement"],
                    category=category,
                    importance=data.get("importance", 0.5),
                    workflow=WorkflowStatus.PENDING,
                    belief=EpistemicStatus.UNVERIFIED,
                    confidence=ConfidenceMetrics(extraction=0.9, retrieval=0.0, analysis=0.0),
                    primary_slide=slide_index,
                    extraction_method="text"
                )
                claims.append(claim)
                
            return claims
            
        except Exception as e:
            logger.error(f"Claim extraction failed for slide {slide_index}: {str(e)}")
            return []
