from langchain_ollama import OllamaLLM
from app.schemas.epistemic import Claim, Evidence, EpistemicStatus, WorkflowStatus
from app.tools.search import SearchService
from typing import List, Dict, Any
import json
import logging
import hashlib
import uuid

logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    Agent responsible for verifying claims by generating adversarial queries 
    and retrieving external evidence.
    """
    
    def __init__(self, model_name: str = "qwen3:8b"):
        self.llm = OllamaLLM(model=model_name, temperature=0.2)
        self.search_service = SearchService()
        
    def _get_query_gen_prompt(self, claim: str, company: str = None) -> str:
        company_context = f" for the company '{company}'" if company else ""
        return f"""You are an Investigative Research Specialist. Your goal is to verify the following startup claim{company_context}.
        
CLAIM: "{claim}"

Generate 3-5 high-signal search queries designed to TRIANGULATE the truth. 
Use an adversarial approach: do not just search for the claim, search for contradictions, competitor benchmarks, and independent verification.

Query types to include:
1. Direct Verification: Verification of the specific metric/fact.
2. Competitor Check: How do competitors or the market average compare?
3. Social Proof/Footprint: Reviews, public mentions, or news coverage.
4. Adversarial Check: Potential exaggerations or complaints.

Return a JSON list of strings. Do not include any preamble.
EXAMPLE: ["competitor market share 2026", "complaints about company X", "independent review of Y technology"]"""

    async def generate_queries(self, claim: Claim, company_name: str = None) -> List[str]:
        """
        Generates adversarial search queries for a claim.
        """
        prompt = self._get_query_gen_prompt(claim.statement, company_name)
        try:
            response = await self.llm.ainvoke(prompt)
            raw_json = response.strip().strip("```json").strip("```").strip()
            queries = json.loads(raw_json)
            return queries
        except Exception as e:
            logger.error(f"Query generation failed for claim {claim.id}: {str(e)}")
            return [claim.statement] # Fallback to literal claim

    async def research_claim(self, claim: Claim, company_name: str = None) -> List[Evidence]:
        """
        Performs full research lifecycle: Query Gen -> Search -> Evidence Normalization.
        """
        logger.info(f"Starting research for claim: {claim.id}")
        
        # 1. Generate Queries
        queries = await self.generate_queries(claim, company_name)
        
        all_evidence = []
        seen_urls = set()
        
        # 2. Execute Searches
        for query in queries:
            search_results = await self.search_service.search(query, max_results=3)
            
            for res in search_results:
                url = str(res.get("url"))
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                
                # Create hash-based ID for evidence deduplication
                content_hash = hashlib.md5(res["content"].encode()).hexdigest()
                
                evidence = Evidence(
                    id=f"ev_{content_hash[:10]}",
                    source_type="web_search",
                    url=res.get("url"),
                    title=res.get("title"),
                    content_snippet=res.get("content"),
                    source_authority=0.5, # Default, will be updated by Analyst
                    recency_score=1.0,
                    relevance_to_claim=res.get("score", 0.8),
                    supports_claim=True # Placeholder, Analyst will determine
                )
                all_evidence.append(evidence)
                
        logger.info(f"Retrieved {len(all_evidence)} evidence pieces for claim {claim.id}")
        return all_evidence
