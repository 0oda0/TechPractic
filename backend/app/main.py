from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.core.elastic import create_index_if_not_exists

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="University Knowledge Search",
    description="Intelligent search system for university knowledge base",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)

#@app.on_event("startup")
#def startup():
#    create_index_if_not_exists()

@app.get("/")
def root():
    return {"message": "University Knowledge Search API"}