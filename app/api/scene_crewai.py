from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.scenes.crewai_scenes import build_pov_scene_crew

router = APIRouter()


class Character(BaseModel):
    name: str
    role: Optional[str] = "персонаж"
    traits: Optional[str] = ""
    background: Optional[str] = ""
    speaking_style: Optional[str] = ""
    private_goals: Optional[str] = ""


class SceneRequest(BaseModel):
    scene_description: str
    characters: List[Character]
    words_min: int = 300
    words_max: int = 700


@router.post("/generate_pov_crewai")
def generate_pov_scene(req: SceneRequest):
    chars = [c.model_dump() for c in req.characters]
    crew = build_pov_scene_crew(
        chars,
        req.scene_description,
        words_min=req.words_min,
        words_max=req.words_max,
    )
    result = crew.kickoff()
    return {"scene_text": str(result)}
