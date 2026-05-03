import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.researcher import ResearchAgent
from app.schemas.epistemic import Claim, ClaimCategory

async def test_researcher():
    researcher = ResearchAgent()
    
    # Create a mock claim
    claim = Claim(
        id="test_clm_001",
        statement="We hold 40% of the Indian EdTech market share.",
        category=ClaimCategory.MARKET_SHARE,
        importance=0.9,
        primary_slide=8,
        extraction_method="text"
    )
    
    print(f"Testing Research Agent for claim: '{claim.statement}'")
    
    # 1. Test Query Generation
    print("\n1. Generating Adversarial Queries...")
    queries = await researcher.generate_queries(claim, "ExampleEd")
    for i, q in enumerate(queries):
        print(f"  Query {i+1}: {q}")
        
    # 2. Test Research Lifecycle
    if not os.getenv("TAVILY_API_KEY"):
        print("\n[WARNING] TAVILY_API_KEY not found. Skipping live search test.")
        return

    print("\n2. Executing Live Research (Tavily)...")
    evidence_list = await researcher.research_claim(claim, "ExampleEd")
    
    print(f"\nRetrieved {len(evidence_list)} evidence items:")
    for i, ev in enumerate(evidence_list[:3]): # Show first 3
        print(f"\nEvidence {i+1}:")
        print(f"  ID: {ev.id}")
        print(f"  Title: {ev.title}")
        print(f"  URL: {ev.url}")
        print(f"  Snippet: {ev.content_snippet[:150]}...")

if __name__ == "__main__":
    try:
        asyncio.run(test_researcher())
    except Exception as e:
        print(f"Error during research test: {e}")
