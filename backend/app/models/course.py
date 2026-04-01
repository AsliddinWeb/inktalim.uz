# Kurs modeli — online kurslarni ifodalaydi
# Har bir kursning tartibi (order) va nashr holati bor

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Course(Base):
    """Kurs jadvali — platforma kurslari."""

    __tablename__ = "courses"

    # Birlamchi kalit — UUID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Kurs nomi
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # Kurs tavsifi — uzun matn
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Muqova rasmi URL (nullable)
    thumbnail_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Nashr holati — False bo'lsa studentlarga ko'rinmaydi
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Kurslar ro'yxatidagi tartib raqami
    order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        index=True,
    )

    # Kursni yaratgan admin (FK → users)
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Yaratilgan vaqt
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Yangilangan vaqt
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Kursni yaratgan foydalanuvchi
    creator: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="courses",
        foreign_keys=[created_by],
    )

    # Kurs modullari (tartib bo'yicha)
    modules: Mapped[list["Module"]] = relationship(  # type: ignore
        "Module",
        back_populates="course",
        order_by="Module.order",
        cascade="all, delete-orphan",
    )

    # Kurs darslari (tartib bo'yicha) — modul orqali ham, to'g'ridan ham
    lessons: Mapped[list["Lesson"]] = relationship(  # type: ignore
        "Lesson",
        back_populates="course",
        order_by="Lesson.order",
        cascade="all, delete-orphan",
    )

    # Kurs bo'yicha progress yozuvlari
    progress_records: Mapped[list["Progress"]] = relationship(  # type: ignore
        "Progress",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    # Kurs sertifikatlari
    certificates: Mapped[list["Certificate"]] = relationship(  # type: ignore
        "Certificate",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Course id={self.id} title={self.title!r} published={self.is_published}>"
