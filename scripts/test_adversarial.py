import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.analyst import AnalystAgent
from app.agents.skeptic import SkepticAgent
from app.core.belief_engine import BeliefEngine
from app.schemas.epistemic import Claim, Evidence, ClaimCategory, GlobalInvestigationState, EpistemicStatus

async def test_adversarial_analysis():
    analyst = AnalystAgent()
    skeptic = SkepticAgent()
    engine = BeliefEngine()
    
    # 1. Setup Mock State
    claim = Claim(
        id="clm_financial_01",
        statement="We achieved $10M ARR in 2025.",
        category=ClaimCategory.FINANCIAL_REVENUE,
        importance=1.0,
        primary_slide=3,
        extraction_method="text"
    )
    
    # Mock Evidence (Contradictory)
    evidence = [
        Evidence(
            id="ev_001",
            source_type="web_search",
            title="TechCrunch Funding News",
            content_snippet="SolarStream announced a $2M Seed round. Revenue is estimated to be around $500k ARR.",
            supports_claim=False
        )
    ]
    
    print(f"--- Adversarial Analysis Test ---")
    print(f"Claim: {claim.statement}")
    
    # 2. Test Analyst
    print("\n1. Running Analyst Agent...")
    status, credibility, confidence = await analyst.analyze_claim(claim, evidence)
    claim.belief = status
    claim.credibility_score = credibility
    claim.confidence = confidence
    
    print(f"  Resulting Status: {claim.belief}")
    print(f"  Credibility Score: {claim.credibility_score}")
    print(f"  Analyst Summary: {claim.analyst_summary}")
    
    # 3. Test Skeptic
    print("\n2. Running Skeptic Agent...")
    skeptic_status, skeptic_score = await skeptic.review_claim(claim, evidence)
    claim.belief = skeptic_status
    
    print(f"  Adversarial Status: {claim.belief}")
    print(f"  Skepticism Score: {skeptic_score}")
    print(f"  Skeptic Summary: {claim.skeptic_summary}")
    
    # 4. Test Belief Engine
    print("\n3. Running Belief Engine (Global Score)...")
    state = GlobalInvestigationState(
        document_id="test_doc",
        claims={claim.id: claim}
    )
    
    global_score = engine.update_global_score(state)
    print(f"  Prior Score: 0.85")
    print(f"  Final Global Credibility: {global_score}")
    print(f"  Red Flags Detected: {state.red_flag_count}")

if __name__ == "__main__":
    try:
        asyncio.run(test_adversarial_analysis())
    except Exception as e:
        print(f"Error during adversarial test: {e}")
