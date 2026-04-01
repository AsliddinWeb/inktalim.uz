# Admin — Quiz CRUD
# Darsga quiz qo'shish, savollar va variantlarni boshqarish
# Faqat adminlar uchun

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.quiz import Choice, Question, Quiz
from app.schemas.quiz import (
    ChoiceCreate,
    ChoiceResponse,
    ChoiceUpdate,
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    QuizCreate,
    QuizResponse,
    QuizUpdate,
    QuizWithQuestionsResponse,
    ReorderRequest,
)

router = APIRouter()


# ─── Quiz ────────────────────────────────────────────────────────────────────

async def _get_quiz_or_404(quiz_id: uuid.UUID, db: AsyncSession) -> Quiz:
    result = await db.execute(
        select(Quiz)
        .where(Quiz.id == quiz_id)
        .options(
            selectinload(Quiz.questions).selectinload(Question.choices)
        )
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz topilmadi")
    return quiz


@router.post("", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    data: QuizCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Quiz:
    """Darsga yangi quiz yaratish (darsda faqat 1 ta bo'lishi mumkin)."""
    # Mavjud quizni tekshirish
    existing = await db.execute(
        select(Quiz).where(Quiz.lesson_id == data.lesson_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu darsda allaqachon quiz mavjud",
        )

    quiz = Quiz(**data.model_dump())
    db.add(quiz)
    await db.commit()
    await db.refresh(quiz)
    return quiz


@router.get("/{quiz_id}", response_model=QuizWithQuestionsResponse)
async def get_quiz(
    quiz_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Quiz:
    """Quiz tafsilotlari (savollar va variantlar bilan)."""
    return await _get_quiz_or_404(quiz_id, db)


@router.get("/by-lesson/{lesson_id}", response_model=QuizWithQuestionsResponse)
async def get_quiz_by_lesson(
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Quiz:
    """Dars ID orqali quizni olish."""
    result = await db.execute(
        select(Quiz)
        .where(Quiz.lesson_id == lesson_id)
        .options(
            selectinload(Quiz.questions).selectinload(Question.choices)
        )
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bu darsda quiz yo'q")
    return quiz


@router.patch("/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
    quiz_id: uuid.UUID,
    data: QuizUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Quiz:
    """Quiz meta ma'lumotlarini yangilash."""
    quiz = await _get_quiz_or_404(quiz_id, db)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(quiz, field, value)
    await db.commit()
    await db.refresh(quiz)
    return quiz


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> None:
    """Quizni o'chirish (savollar va variantlar kaskad o'chadi)."""
    quiz = await _get_quiz_or_404(quiz_id, db)
    await db.delete(quiz)
    await db.commit()


# ─── Question ────────────────────────────────────────────────────────────────

async def _get_question_or_404(question_id: uuid.UUID, db: AsyncSession) -> Question:
    result = await db.execute(
        select(Question)
        .where(Question.id == question_id)
        .options(selectinload(Question.choices))
    )
    q = result.scalar_one_or_none()
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Savol topilmadi")
    return q


@router.post("/{quiz_id}/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    quiz_id: uuid.UUID,
    data: QuestionCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Question:
    """Quizga yangi savol qo'shish (variantlar bilan birga)."""
    # Quiz mavjudligini tekshirish
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz topilmadi")

    question = Question(
        quiz_id=quiz_id,
        text=data.text,
        order=data.order,
    )
    db.add(question)
    await db.flush()  # question.id kerak bo'ladi

    for choice_data in data.choices:
        choice = Choice(question_id=question.id, **choice_data.model_dump())
        db.add(choice)

    await db.commit()

    # Fresh load with choices
    result = await db.execute(
        select(Question)
        .where(Question.id == question.id)
        .options(selectinload(Question.choices))
    )
    return result.scalar_one()


@router.patch("/{quiz_id}/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    quiz_id: uuid.UUID,
    question_id: uuid.UUID,
    data: QuestionUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Question:
    """Savol matnini yoki tartibini yangilash."""
    question = await _get_question_or_404(question_id, db)
    if question.quiz_id != quiz_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Savol topilmadi")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(question, field, value)
    await db.commit()
    await db.refresh(question)
    return question


@router.delete("/{quiz_id}/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    quiz_id: uuid.UUID,
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> None:
    """Savolni o'chirish (variantlar kaskad o'chadi)."""
    question = await _get_question_or_404(question_id, db)
    if question.quiz_id != quiz_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Savol topilmadi")
    await db.delete(question)
    await db.commit()


@router.post("/{quiz_id}/questions/reorder", status_code=status.HTTP_204_NO_CONTENT)
async def reorder_questions(
    quiz_id: uuid.UUID,
    data: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> None:
    """Savollar tartibini o'zgartirish."""
    result = await db.execute(
        select(Question).where(Question.quiz_id == quiz_id)
    )
    questions = {q.id: q for q in result.scalars().all()}

    for item in data.items:
        if item.id in questions:
            questions[item.id].order = item.order

    await db.commit()


# ─── Choice ──────────────────────────────────────────────────────────────────

async def _get_choice_or_404(choice_id: uuid.UUID, db: AsyncSession) -> Choice:
    result = await db.execute(select(Choice).where(Choice.id == choice_id))
    c = result.scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant topilmadi")
    return c


@router.post(
    "/{quiz_id}/questions/{question_id}/choices",
    response_model=ChoiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_choice(
    quiz_id: uuid.UUID,
    question_id: uuid.UUID,
    data: ChoiceCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Choice:
    """Savolga yangi variant qo'shish."""
    question = await _get_question_or_404(question_id, db)
    if question.quiz_id != quiz_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Savol topilmadi")

    choice = Choice(question_id=question_id, **data.model_dump())
    db.add(choice)
    await db.commit()
    await db.refresh(choice)
    return choice


@router.patch(
    "/{quiz_id}/questions/{question_id}/choices/{choice_id}",
    response_model=ChoiceResponse,
)
async def update_choice(
    quiz_id: uuid.UUID,
    question_id: uuid.UUID,
    choice_id: uuid.UUID,
    data: ChoiceUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Choice:
    """Variant matnini yoki to'g'riligini yangilash."""
    choice = await _get_choice_or_404(choice_id, db)
    if choice.question_id != question_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant topilmadi")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(choice, field, value)
    await db.commit()
    await db.refresh(choice)
    return choice


@router.delete(
    "/{quiz_id}/questions/{question_id}/choices/{choice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_choice(
    quiz_id: uuid.UUID,
    question_id: uuid.UUID,
    choice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> None:
    """Variantni o'chirish."""
    choice = await _get_choice_or_404(choice_id, db)
    if choice.question_id != question_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant topilmadi")
    await db.delete(choice)
    await db.commit()
