from fastapi import FastAPI

from backend.routes import router

app = FastAPI(
    title="AI Data Science Operating System",
    version="1.0",
    description="Autonomous Multi-Agent AI Data Science Platform"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI Data Science Operating System API is running",
        "version": "1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI-DS OS"
    }