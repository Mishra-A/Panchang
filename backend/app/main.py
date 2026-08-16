from fastapi import FastAPI

from backend.app.api.panchang import router as panchang_router


app = FastAPI(
    title="Panchang AI API",
    version="0.1.0",
    description="Panchang, Kaal and Muhurat calculation API",
)


app.include_router(
    panchang_router
)


@app.get("/")
def root():
    return {
        "message": "Panchang AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "panchang-api",
    }