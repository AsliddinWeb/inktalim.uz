# Quiz urinish modellari — QuizAttempt, AttemptAnswer
# Bir foydalanuvchi bir quizga bir necha marta urinishi mumkin

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class QuizAttempt(Base):
    """Quiz urinish jadvali — har bir urinish natijasi."""

    __tablename__ = "quiz_attempts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Qaysi quizga tegishli (FK → quizzes)
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Qaysi foydalanuvchi (FK → users)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Ball foizi (0.0 – 100.0)
    score_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    # O'tdimi yoki yo'qmi (pass_percent bilan solishtiriladi)
    is_passed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Tugatilgan vaqt
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Tegishli quiz
    quiz: Mapped["Quiz"] = relationship(  # type: ignore
        "Quiz",
        back_populates="attempts",
    )

    # Tegishli foydalanuvchi
    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="quiz_attempts",
    )

    # Urinish javoblari
    answers: Mapped[list["AttemptAnswer"]] = relationship(
        "AttemptAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<QuizAttempt id={self.id} "
            f"score={self.score_percent:.1f}% "
            f"passed={self.is_passed}>"
        )


class AttemptAnswer(Base):
    """Urinish javobi jadvali — har bir savol uchun tanlangan variant."""

    __tablename__ = "attempt_answers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Qaysi urinishga tegishli (FK → quiz_attempts)
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quiz_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Qaysi savolga (FK → questions)
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Tanlangan variant (FK → choices)
    choice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("choices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Tegishli urinish
    attempt: Mapped["QuizAttempt"] = relationship(
        "QuizAttempt",
        back_populates="answers",
    )

    # Tegishli savol
    question: Mapped["Question"] = relationship(  # type: ignore
        "Question",
        back_populates="attempt_answers",
    )

    # Tanlangan variant
    choice: Mapped["Choice"] = relationship(  # type: ignore
        "Choice",
        back_populates="attempt_answers",
    )

    def __repr__(self) -> str:
        return f"<AttemptAnswer attempt={self.attempt_id} question={self.question_id}>"
