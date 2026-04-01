# Foydalanuvchi modeli — platforma foydalanuvchilari va adminlar
# UUID birlamchi kalit, O'zbekiston telefon formati: +998XXXXXXXXX

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """Foydalanuvchi jadvali — student va admin rollari."""

    __tablename__ = "users"

    # Birlamchi kalit — UUID (raqamli ID dan xavfsizroq)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # To'liq ism
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Email — noyob va indekslangan
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # Telefon raqami — O'zbekiston formati +998XXXXXXXXX
    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    # Xeshlangan parol — ochiq matn saqlanmaydi!
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Faollik holati — False bo'lsa login qila olmaydi
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Admin roli — True bo'lsa barcha CRUD amallarni bajara oladi
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Profil rasmi URL (nullable)
    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Yaratilgan vaqt — avtomatik o'rnatiladi
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Yangilangan vaqt — har o'zgarishda avtomatik yangilanadi
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Bog'liq kurslar (admin tomonidan yaratilganlar)
    courses: Mapped[list["Course"]] = relationship(  # type: ignore
        "Course",
        back_populates="creator",
        foreign_keys="Course.created_by",
    )

    # Foydalanuvchi progressi
    progress_records: Mapped[list["Progress"]] = relationship(  # type: ignore
        "Progress",
        back_populates="user",
    )

    # Quiz urinishlari
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(  # type: ignore
        "QuizAttempt",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Sertifikatlar
    certificates: Mapped[list["Certificate"]] = relationship(  # type: ignore
        "Certificate",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} admin={self.is_admin}>"
