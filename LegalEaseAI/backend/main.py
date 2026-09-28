from fastapi import FastAPI
from backend.routes import router

app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "LegalEase API is running"
    }


app.include_router(router)
