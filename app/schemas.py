from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class CharacterBase(BaseModel):
    name: str
    role: Optional[str] = None
    traits: Optional[str] = None
    background: Optional[str] = None
    speaking_style: Optional[str] = None
    private_goals: Optional[str] = None


class CharacterCreate(CharacterBase):
    pass


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    traits: Optional[str] = None
    background: Optional[str] = None
    speaking_style: Optional[str] = None
    private_goals: Optional[str] = None


class CharacterOut(CharacterBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class POVRequest(BaseModel):
    scene_description: str
    character_ids: List[int]
    words_min: Optional[int] = None
    words_max: Optional[int] = None


class POVResult(BaseModel):
    character_id: int
    character_name: str
    pov_text: str


class POVResponse(BaseModel):
    results: List[POVResult]


class DialogueRequest(BaseModel):
    scene_description: str
    character_ids: List[int]
    turns: int = 3


class DialogueTurn(BaseModel):
    character_id: int
    character_name: str
    utterance: str


class DialogueResponse(BaseModel):
    dialogue_text: str
    turns: List[DialogueTurn]


class BookPlanRequest(BaseModel):
    genre: str
    target_length: str
    main_characters: List[int]
    tone: Optional[str] = None
    setting: Optional[str] = None


class ChapterInfo(BaseModel):
    number: int
    title: str
    summary: str


class BookPlanResponse(BaseModel):
    synopsis: str
    chapters: List[ChapterInfo]


class ChapterGenerationRequest(BaseModel):
    book_plan: BookPlanResponse
    chapter_number: int
    active_characters: List[int]


class ChapterGenerationResponse(BaseModel):
    chapter_text: str
