import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import characters, scenes, books
from app.api import scene_crewai

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="book-multiagent-codex", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(characters.router)
app.include_router(scenes.router)
app.include_router(books.router)
app.include_router(scene_crewai.router, prefix="/scene", tags=["scene_crewai"])
