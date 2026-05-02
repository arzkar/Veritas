import os
from typing import List, Dict, Any
from tavily import TavilyClient
import logging
from dotenv import load_dotenv

# Load environment variables
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(root_dir, ".env")
app_dotenv_path = os.path.join(root_dir, "app", ".env")

load_dotenv(dotenv_path=dotenv_path)
load_dotenv(dotenv_path=app_dotenv_path)

logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for external information retrieval using Tavily and other search APIs.
    """
    
    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        if self.tavily_api_key:
            self.tavily = TavilyClient(api_key=self.tavily_api_key)
        else:
            logger.warning("TAVILY_API_KEY not found in environment. Search will fail.")
            self.tavily = None

    async def search(self, query: str, search_depth: str = "advanced", max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Performs a search using Tavily.
        Returns a list of structured results.
        """
        if not self.tavily:
            logger.error("Search attempted but Tavily client not initialized.")
            return []
            
        try:
            # Tavily's python client is synchronous, so we run in executor or just call it if low volume
            # For MVP, we'll call it directly
            response = self.tavily.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                include_answer=True,
                include_raw_content=False
            )
            
            results = []
            for res in response.get("results", []):
                results.append({
                    "url": res.get("url"),
                    "title": res.get("title"),
                    "content": res.get("content"),
                    "score": res.get("score", 0.0),
                    "raw_answer": response.get("answer") # Shared answer context
                })
            return results
            
        except Exception as e:
            logger.error(f"Tavily search failed for query '{query}': {str(e)}")
            return []
