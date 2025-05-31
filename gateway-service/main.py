from fastapi import FastAPI
from router import prompt_routing
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt_routing.prompt_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8080, log_level="info")