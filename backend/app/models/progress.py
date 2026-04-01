# Progress modeli — foydalanuvchi dars ko'rish tarixi
# UniqueConstraint: bir foydalanuvchi bir darsni faqat bir marta belgilaydi

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Progress(Base):
    """Progress jadvali — foydalanuvchi dars tugatish holati."""

    __tablename__ = "progress"

    # Jadval darajasida cheklov — bir foydalanuvchi + bir dars = yagona yozuv
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "lesson_id",
            name="uq_progress_user_lesson",
        ),
    )

    # Birlamchi kalit — UUID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Qaysi foydalanuvchi (FK → users)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Qaysi dars (FK → lessons)
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Qaysi kurs (denormalizatsiya — progress hisoblash tezroq bo'lsin)
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Dars tugatilganmi?
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Tugatilgan vaqt (nullable — tugatilinmagan bo'lsa None)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Yozuv yaratilgan vaqt
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Foydalanuvchi (relationship)
    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="progress_records",
    )

    # Dars (relationship)
    lesson: Mapped["Lesson"] = relationship(  # type: ignore
        "Lesson",
        back_populates="progress_records",
    )

    # Kurs (relationship)
    course: Mapped["Course"] = relationship(  # type: ignore
        "Course",
        back_populates="progress_records",
    )

    def __repr__(self) -> str:
        return (
            f"<Progress user={self.user_id} lesson={self.lesson_id} "
            f"completed={self.is_completed}>"
        )
