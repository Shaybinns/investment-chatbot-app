from typing import Dict, List
import httpx

class ResearchEngine:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"

    async def research_company(self, symbol: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/analyze",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"query": f"Comprehensive analysis of {symbol} stock"}
            )
            return response.json()