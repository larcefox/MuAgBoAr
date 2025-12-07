from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/characters", tags=["characters"])


@router.post("", response_model=schemas.CharacterOut)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    db_character = models.Character(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


@router.get("", response_model=list[schemas.CharacterOut])
def list_characters(db: Session = Depends(get_db)):
    return db.query(models.Character).all()


@router.get("/{character_id}", response_model=schemas.CharacterOut)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.put("/{character_id}", response_model=schemas.CharacterOut)
def update_character(character_id: int, payload: schemas.CharacterUpdate, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(character, field, value)
    db.commit()
    db.refresh(character)
    return character


@router.delete("/{character_id}")
def delete_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(character)
    db.commit()
    return {"ok": True}
