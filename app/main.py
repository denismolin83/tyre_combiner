from fastapi import FastAPI
from app.api.v1.imports import router as imports_router

app = FastAPI(title="Tyre Combiner Engine")

app.include_router(imports_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
