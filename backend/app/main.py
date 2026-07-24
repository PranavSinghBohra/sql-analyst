from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.query import router

app = FastAPI(title="SQL Analyst")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}