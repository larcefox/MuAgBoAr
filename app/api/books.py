from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.llm import get_llm_client
from app.engines.book_engine import generate_book_plan, parse_plan_response, generate_chapter

router = APIRouter(prefix="/book", tags=["book"])


@router.post("/plan", response_model=schemas.BookPlanResponse)
async def plan_book(payload: schemas.BookPlanRequest, db: Session = Depends(get_db)):
    characters = db.query(models.Character).filter(models.Character.id.in_(payload.main_characters)).all()
    if len(characters) != len(payload.main_characters):
        raise HTTPException(status_code=404, detail="One or more characters not found")
    llm_client = get_llm_client()
    raw_plan = await generate_book_plan(
        llm_client=llm_client,
        genre=payload.genre,
        target_length=payload.target_length,
        characters=characters,
        tone=payload.tone or "",
        setting=payload.setting or "",
    )
    synopsis, chapters = parse_plan_response(raw_plan)
    # store plan in DB
    book_plan = models.BookPlan(
        genre=payload.genre,
        synopsis=synopsis,
        target_length=payload.target_length,
        main_characters=",".join([str(cid) for cid in payload.main_characters]),
        tone=payload.tone,
        setting=payload.setting,
    )
    db.add(book_plan)
    db.commit()
    db.refresh(book_plan)
    return {"plan_id": book_plan.id, "synopsis": synopsis, "chapters": chapters}


@router.post("/generate_chapter", response_model=schemas.ChapterGenerationResponse)
async def generate_chapter_endpoint(payload: schemas.ChapterGenerationRequest, db: Session = Depends(get_db)):
    characters = db.query(models.Character).filter(models.Character.id.in_(payload.active_characters)).all()
    if len(characters) != len(payload.active_characters):
        raise HTTPException(status_code=404, detail="One or more characters not found")
    llm_client = get_llm_client()
    plan_dict = payload.book_plan.model_dump()
    plan_id = payload.book_plan_id
    if not plan_id:
        # если план не сохранён — создаём черновик в БД
        book_plan = models.BookPlan(
            genre="unknown",
            synopsis=plan_dict.get("synopsis") or "",
            target_length="",
            main_characters=",".join([str(cid) for cid in payload.active_characters]),
            tone="",
            setting="",
        )
        db.add(book_plan)
        db.commit()
        db.refresh(book_plan)
        plan_id = book_plan.id

    chapter_text = await generate_chapter(llm_client, plan_dict, payload.chapter_number, characters)
    # сохранить/обновить главу
    chapter = (
        db.query(models.Chapter)
        .filter(models.Chapter.book_plan_id == plan_id, models.Chapter.chapter_number == payload.chapter_number)
        .first()
    )
    summary = ""
    title = ""
    for ch in plan_dict.get("chapters", []):
        if ch.get("number") == payload.chapter_number:
            title = ch.get("title") or ""
            summary = ch.get("summary") or ""
            break
    if chapter:
        chapter.full_text = chapter_text
        chapter.title = title
        chapter.summary = summary
    else:
        chapter = models.Chapter(
            book_plan_id=plan_id,
            chapter_number=payload.chapter_number,
            title=title,
            summary=summary,
            full_text=chapter_text,
        )
        db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return {"chapter_text": chapter_text, "chapter_id": chapter.id}
