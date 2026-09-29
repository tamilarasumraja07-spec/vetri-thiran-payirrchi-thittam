from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routes import auth, pages, planners, session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-powered budget and recommendation assistant "
        "for home interiors, parties and jewelry."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    session.router
)

app.include_router(
    planners.router
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": settings.APP_NAME,
    }