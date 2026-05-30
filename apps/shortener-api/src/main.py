from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import health, urls

app = FastAPI(title="Nimbus Shortener API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(urls.router)