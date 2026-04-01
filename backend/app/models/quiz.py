# Quiz tizimi modellari — Quiz, Question, Choice
# Har bir darsda maksimal 1 ta quiz bo'lishi mumkin (lesson_id unique)

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Quiz(Base):
    """Quiz jadvali — har bir dars uchun test."""

    __tablename__ = "quizzes"

    __table_args__ = (
        # Har bir darsda faqat bitta quiz bo'lishi mumkin
        UniqueConstraint("lesson_id", name="uq_quiz_lesson"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Qaysi darsga tegishli (FK → lessons)
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Quiz sarlavhasi
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # Qo'shimcha tavsif (ixtiyoriy)
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # O'tish uchun minimal foiz (masalan 60 = 60%)
    pass_percent: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    # Faollik holati — False bo'lsa studentlarga ko'rinmaydi
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Savollar (relationship)
    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="Question.order",
    )

    # Urinishlar (relationship)
    attempts: Mapped[list["QuizAttempt"]] = relationship(  # type: ignore
        "QuizAttempt",
        back_populates="quiz",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Quiz id={self.id} title={self.title!r} lesson={self.lesson_id}>"


class Question(Base):
    """Savol jadvali — har bir quizning savollar to'plami."""

    __tablename__ = "questions"

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

    # Savol matni
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Quiz ichidagi tartib raqami
    order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Tegishli quiz
    quiz: Mapped["Quiz"] = relationship(
        "Quiz",
        back_populates="questions",
    )

    # Javob variantlari
    choices: Mapped[list["Choice"]] = relationship(
        "Choice",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="Choice.order",
    )

    # Attempt javoblari
    attempt_answers: Mapped[list["AttemptAnswer"]] = relationship(  # type: ignore
        "AttemptAnswer",
        back_populates="question",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Question id={self.id} order={self.order}>"


class Choice(Base):
    """Javob varianti jadvali — har bir savolning variantlari."""

    __tablename__ = "choices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Qaysi savolga tegishli (FK → questions)
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Variant matni
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # To'g'ri javobmi?
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Tartib raqami
    order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # Tegishli savol
    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="choices",
    )

    # Attempt javoblari
    attempt_answers: Mapped[list["AttemptAnswer"]] = relationship(  # type: ignore
        "AttemptAnswer",
        back_populates="choice",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Choice id={self.id} correct={self.is_correct}>"
