# Quiz urinish sxemalari — submit, natija, tarix

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AnswerSubmit(BaseModel):
    """Bitta savol uchun javob."""
    question_id: uuid.UUID
    choice_id: uuid.UUID


class SubmitQuizRequest(BaseModel):
    """Student quizni topshirish uchun yuboradigan ma'lumot."""
    answers: list[AnswerSubmit] = Field(..., min_length=1)


class AnswerResult(BaseModel):
    """Natijadagi har bir javob tafsiloti."""
    question_id: uuid.UUID
    question_text: str
    selected_choice_id: uuid.UUID
    selected_choice_text: str
    correct_choice_id: uuid.UUID
    correct_choice_text: str
    is_correct: bool


class AttemptResultResponse(BaseModel):
    """Quiz topshirish natijasi."""
    attempt_id: uuid.UUID
    quiz_id: uuid.UUID
    score_percent: float
    is_passed: bool
    pass_percent: int
    correct_count: int
    total_count: int
    completed_at: datetime
    answers: list[AnswerResult] = []

    model_config = {"from_attributes": True}


class AttemptHistoryItem(BaseModel):
    """Tarix ro'yxati uchun qisqacha ma'lumot."""
    attempt_id: uuid.UUID
    score_percent: float
    is_passed: bool
    completed_at: datetime

    model_config = {"from_attributes": True}


class AttemptHistoryResponse(BaseModel):
    """Student uchun quiz urinishlari tarixi."""
    quiz_id: uuid.UUID
    quiz_title: str
    pass_percent: int
    attempts: list[AttemptHistoryItem] = []
    best_score: float | None = None
    last_attempt: AttemptHistoryItem | None = None
