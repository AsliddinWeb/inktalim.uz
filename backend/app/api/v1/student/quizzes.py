# Student — Quiz
# Dars quizini ko'rish, topshirish va natijalar tarixi
# Faqat ro'yxatdan o'tgan foydalanuvchilar uchun

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.quiz import Choice, Question, Quiz
from app.models.quiz_attempt import AttemptAnswer, QuizAttempt
from app.models.user import User
from app.schemas.quiz import QuizForStudentResponse
from app.schemas.quiz_attempt import (
    AnswerResult,
    AttemptHistoryItem,
    AttemptHistoryResponse,
    AttemptResultResponse,
    SubmitQuizRequest,
)

router = APIRouter()


@router.get("/by-lesson/{lesson_id}", response_model=QuizForStudentResponse)
async def get_quiz_for_lesson(
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Quiz:
    """Dars uchun quizni olish (is_correct yashiriladi)."""
    result = await db.execute(
        select(Quiz)
        .where(Quiz.lesson_id == lesson_id, Quiz.is_active.is_(True))
        .options(
            selectinload(Quiz.questions).selectinload(Question.choices)
        )
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu darsda quiz mavjud emas",
        )
    return quiz


@router.post("/by-lesson/{lesson_id}/submit", response_model=AttemptResultResponse)
async def submit_quiz(
    lesson_id: uuid.UUID,
    data: SubmitQuizRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AttemptResultResponse:
    """Quizni topshirish — natija va ball hisoblanadi."""
    # Quizni olish
    result = await db.execute(
        select(Quiz)
        .where(Quiz.lesson_id == lesson_id, Quiz.is_active.is_(True))
        .options(
            selectinload(Quiz.questions).selectinload(Question.choices)
        )
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu darsda quiz mavjud emas",
        )

    # Savollar va to'g'ri variantlar indeksi
    questions_map: dict[uuid.UUID, Question] = {q.id: q for q in quiz.questions}
    correct_map: dict[uuid.UUID, Choice] = {}
    choices_map: dict[uuid.UUID, Choice] = {}

    for question in quiz.questions:
        for choice in question.choices:
            choices_map[choice.id] = choice
            if choice.is_correct:
                correct_map[question.id] = choice

    # Javoblarni tekshirish
    total = len(questions_map)
    if total == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quizda savollar mavjud emas",
        )

    correct_count = 0
    answer_results: list[AnswerResult] = []

    for answer in data.answers:
        question = questions_map.get(answer.question_id)
        selected_choice = choices_map.get(answer.choice_id)

        if not question or not selected_choice:
            continue

        correct_choice = correct_map.get(answer.question_id)
        is_correct = (
            correct_choice is not None
            and answer.choice_id == correct_choice.id
        )
        if is_correct:
            correct_count += 1

        answer_results.append(
            AnswerResult(
                question_id=question.id,
                question_text=question.text,
                selected_choice_id=selected_choice.id,
                selected_choice_text=selected_choice.text,
                correct_choice_id=correct_choice.id if correct_choice else selected_choice.id,
                correct_choice_text=correct_choice.text if correct_choice else "",
                is_correct=is_correct,
            )
        )

    score_percent = round(correct_count / total * 100, 1)
    is_passed = score_percent >= quiz.pass_percent

    # Urinishni saqlash
    attempt = QuizAttempt(
        quiz_id=quiz.id,
        user_id=current_user.id,
        score_percent=score_percent,
        is_passed=is_passed,
    )
    db.add(attempt)
    await db.flush()

    # Javoblarni saqlash
    for answer in data.answers:
        if answer.question_id in questions_map and answer.choice_id in choices_map:
            db.add(AttemptAnswer(
                attempt_id=attempt.id,
                question_id=answer.question_id,
                choice_id=answer.choice_id,
            ))

    # O'tgan bo'lsa — dars progressini yangilash
    if is_passed:
        progress_result = await db.execute(
            select(Progress).where(
                Progress.user_id == current_user.id,
                Progress.lesson_id == lesson_id,
            )
        )
        progress = progress_result.scalar_one_or_none()
        if progress and not progress.is_completed:
            progress.is_completed = True

    await db.commit()

    return AttemptResultResponse(
        attempt_id=attempt.id,
        quiz_id=quiz.id,
        score_percent=score_percent,
        is_passed=is_passed,
        pass_percent=quiz.pass_percent,
        correct_count=correct_count,
        total_count=total,
        completed_at=attempt.completed_at,
        answers=answer_results,
    )


@router.get("/by-lesson/{lesson_id}/history", response_model=AttemptHistoryResponse)
async def get_attempt_history(
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AttemptHistoryResponse:
    """Foydalanuvchining quiz urinishlari tarixi."""
    # Quizni olish
    result = await db.execute(
        select(Quiz).where(Quiz.lesson_id == lesson_id)
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu darsda quiz mavjud emas",
        )

    # Urinishlarni olish
    attempts_result = await db.execute(
        select(QuizAttempt)
        .where(
            QuizAttempt.quiz_id == quiz.id,
            QuizAttempt.user_id == current_user.id,
        )
        .order_by(QuizAttempt.completed_at.desc())
    )
    attempts = attempts_result.scalars().all()

    history_items = [
        AttemptHistoryItem(
            attempt_id=a.id,
            score_percent=a.score_percent,
            is_passed=a.is_passed,
            completed_at=a.completed_at,
        )
        for a in attempts
    ]

    best_score = max((a.score_percent for a in attempts), default=None)
    last_attempt = history_items[0] if history_items else None

    return AttemptHistoryResponse(
        quiz_id=quiz.id,
        quiz_title=quiz.title,
        pass_percent=quiz.pass_percent,
        attempts=history_items,
        best_score=best_score,
        last_attempt=last_attempt,
    )
