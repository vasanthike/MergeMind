from fastapi import FastAPI

from app.webhook import router as webhook_router

app = FastAPI(
    title="MergeMind Backend",
    description="AI-powered GitHub Pull Request review assistant",
    version="0.1.0",
)

app.include_router(webhook_router)


@app.get("/")
def root():
    return {
        "service": "MergeMind",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
