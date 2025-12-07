from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.llm import get_llm_client
from app.engines.scene_engine import generate_pov_scene, generate_dialogue_scene

router = APIRouter(prefix="/scene", tags=["scene"])


@router.post("/generate_pov", response_model=schemas.POVResponse)
async def generate_pov_endpoint(payload: schemas.POVRequest, db: Session = Depends(get_db)):
    characters = db.query(models.Character).filter(models.Character.id.in_(payload.character_ids)).all()
    if len(characters) != len(payload.character_ids):
        raise HTTPException(status_code=404, detail="One or more characters not found")
    llm_client = get_llm_client()
    results = await generate_pov_scene(
        scene_description=payload.scene_description,
        characters=characters,
        llm_client=llm_client,
        words_min=payload.words_min,
        words_max=payload.words_max,
    )
    return {"results": results}


@router.post("/generate_dialogue", response_model=schemas.DialogueResponse)
async def generate_dialogue_endpoint(payload: schemas.DialogueRequest, db: Session = Depends(get_db)):
    characters = db.query(models.Character).filter(models.Character.id.in_(payload.character_ids)).all()
    if len(characters) != len(payload.character_ids):
        raise HTTPException(status_code=404, detail="One or more characters not found")
    llm_client = get_llm_client()
    dialogue_text, turns = await generate_dialogue_scene(
        scene_description=payload.scene_description,
        characters=characters,
        llm_client=llm_client,
        turns=payload.turns,
    )
    return {"dialogue_text": dialogue_text, "turns": turns}
