# Quiz sxemalari — CRUD va student ko'rinishlar
# Admin: is_correct ko'rinadi | Student: is_correct yashiriladi

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# ─────────────────────── Choice ───────────────────────

class ChoiceCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    is_correct: bool = False
    order: int = Field(default=0, ge=0)


class ChoiceUpdate(BaseModel):
    text: str | None = Field(None, min_length=1, max_length=1000)
    is_correct: bool | None = None
    order: int | None = Field(None, ge=0)


class ChoiceResponse(BaseModel):
    """Admin uchun — is_correct ko'rinadi."""
    id: uuid.UUID
    question_id: uuid.UUID
    text: str
    is_correct: bool
    order: int

    model_config = {"from_attributes": True}


class ChoiceForStudent(BaseModel):
    """Student uchun — is_correct yashiriladi."""
    id: uuid.UUID
    question_id: uuid.UUID
    text: str
    order: int

    model_config = {"from_attributes": True}


# ─────────────────────── Question ───────────────────────

class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    order: int = Field(default=0, ge=0)
    choices: list[ChoiceCreate] = Field(default_factory=list)


class QuestionUpdate(BaseModel):
    text: str | None = Field(None, min_length=1, max_length=2000)
    order: int | None = Field(None, ge=0)


class QuestionResponse(BaseModel):
    """Admin uchun — to'liq ma'lumot."""
    id: uuid.UUID
    quiz_id: uuid.UUID
    text: str
    order: int
    created_at: datetime
    choices: list[ChoiceResponse] = []

    model_config = {"from_attributes": True}


class QuestionForStudent(BaseModel):
    """Student uchun — is_correct yashirilgan."""
    id: uuid.UUID
    text: str
    order: int
    choices: list[ChoiceForStudent] = []

    model_config = {"from_attributes": True}


# ─────────────────────── Quiz ───────────────────────

class QuizCreate(BaseModel):
    lesson_id: uuid.UUID
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    pass_percent: int = Field(default=60, ge=0, le=100)
    is_active: bool = True


class QuizUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = None
    pass_percent: int | None = Field(None, ge=0, le=100)
    is_active: bool | None = None


class QuizResponse(BaseModel):
    """Admin uchun — savolsiz, faqat meta ma'lumot."""
    id: uuid.UUID
    lesson_id: uuid.UUID
    title: str
    description: str | None
    pass_percent: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class QuizWithQuestionsResponse(QuizResponse):
    """Admin uchun — savollar va to'g'ri javoblar bilan."""
    questions: list[QuestionResponse] = []


class QuizForStudentResponse(BaseModel):
    """Student uchun — is_correct yashirilgan."""
    id: uuid.UUID
    lesson_id: uuid.UUID
    title: str
    description: str | None
    pass_percent: int
    questions: list[QuestionForStudent] = []

    model_config = {"from_attributes": True}


# ─────────────────────── Reorder ───────────────────────

class ReorderItem(BaseModel):
    id: uuid.UUID
    order: int = Field(..., ge=0)


class ReorderRequest(BaseModel):
    items: list[ReorderItem]
