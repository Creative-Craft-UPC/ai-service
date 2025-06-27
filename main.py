from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.database import test_connection
from routes import prompt_routes
from fastapi.middleware.cors import CORSMiddleware
import os

from google.cloud import storage

storage_client = storage.Client()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio (startup)
    await test_connection()
    yield
    # Evento de cierre (shutdown)
    print("Cerrando la aplicación...")


app = FastAPI(title="AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt_routes.router, prefix="/api/model", tags=["llm-model"])