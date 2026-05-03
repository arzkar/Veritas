import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.extractor import ExtractorAgent

async def test_extractor():
    extractor = ExtractorAgent()
    
    test_text = """
    Slide 4: Traction & Growth
    - We have achieved $2.4M ARR as of Dec 2025.
    - Our user base grew by 40% MoM for the last 6 months.
    - We are the most amazing fintech company in the world.
    - Partnered with AWS and Stripe for infrastructure.
    - Currently 15 full-time employees based in London.
    """
    
    print("Testing Extractor Agent with sample text...")
    claims = await extractor.extract_claims(test_text, 4)
    
    if not claims:
        print("No claims extracted. Check if Ollama is running and qwen2.5:8b is pulled.")
        return

    print(f"\nExtracted {len(claims)} claims:")
    for i, claim in enumerate(claims):
        print(f"\nClaim {i+1}:")
        print(f"  Statement: {claim.statement}")
        print(f"  Category: {claim.category}")
        print(f"  Importance: {claim.importance}")
        print(f"  Slide: {claim.primary_slide}")

if __name__ == "__main__":
    try:
        asyncio.run(test_extractor())
    except Exception as e:
        print(f"Error during test: {e}")
