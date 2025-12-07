import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=True)
    traits = Column(Text, nullable=True)
    background = Column(Text, nullable=True)
    speaking_style = Column(Text, nullable=True)
    private_goals = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class BookPlan(Base):
    __tablename__ = "book_plans"

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String(100), nullable=False)
    synopsis = Column(Text, nullable=False)
    target_length = Column(String(50), nullable=True)
    main_characters = Column(Text, nullable=True)
    tone = Column(String(100), nullable=True)
    setting = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    book_plan_id = Column(Integer, nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=True)
    summary = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
