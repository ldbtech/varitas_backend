from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.api_news import article_fetcher
from services.prompt_analysis import PromptAnalysis
import httpx

app = FastAPI(
    title="Agent Service",
    description="Service for handling agent-related operations",
    version="1.0.0"
)

class PromptRequest(BaseModel):
    prompt: str

class NewsSearchRequest(BaseModel):
    keyword: str
    language: Optional[str] = 'en'
    sort_by: Optional[str] = 'relevancy'
    page_size: Optional[int] = 10
    page: Optional[int] = 1

@app.post("/process_prompt")
async def process_prompt(request: PromptRequest):
    try:
        # Use your existing PromptAnalysis class
        analyzer = PromptAnalysis(request.prompt)
        keyword = analyzer.extract_keywords()
        print(f"Extracted the word: {keyword}")
        
        # Use the search_news endpoint internally
        async with httpx.AsyncClient() as client:
            news_response = await client.post(
                "http://localhost:8001/search_news",
                json={
                    "keyword": keyword,
                    "page_size": 5
                }
            )
            news_response.raise_for_status()
            references = news_response.json()
        
        return {
            "status": "success",
            "keywords": keyword,
            "references": references
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search_news")
async def search_news(request: NewsSearchRequest):
    try:
        article_fetcher.getting_search_result(
            search_keyword=request.keyword,
            language=request.language,
            sort_by=request.sort_by,
            page_size=request.page_size,
            page=request.page
        )

        all_references = article_fetcher.get_url_references()


        return {
            "status": "success",
            "references": all_references
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
