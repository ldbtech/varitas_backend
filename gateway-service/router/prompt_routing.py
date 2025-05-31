from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

class PromptRequest(BaseModel):
    prompt: str

prompt_router = APIRouter(
    tags=["prompts"],
    responses={404: {"description": "Page not found"}},
)

AGENT_SERVICE_URL = "http://localhost:8001"  # Default port for agent-service

@prompt_router.post('/prompt_eng')
async def read_prompt(request: PromptRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AGENT_SERVICE_URL}/process_prompt",
                json={"prompt": request.prompt}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with agent service: {str(e)}")