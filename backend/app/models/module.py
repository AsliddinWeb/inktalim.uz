# Modul modeli — har bir kurs bir necha moduldan iborat
# Har bir modul bir necha darsni o'z ichiga oladi

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Module(Base):
    """Modul jadvali — kurs bo'limlari."""

    __tablename__ = "modules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)

    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Tegishli kurs
    course: Mapped["Course"] = relationship(  # type: ignore
        "Course", back_populates="modules"
    )

    # Modul darslari
    lessons: Mapped[list["Lesson"]] = relationship(  # type: ignore
        "Lesson",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Lesson.order",
    )

    def __repr__(self) -> str:
        return f"<Module id={self.id} title={self.title!r} order={self.order}>"
