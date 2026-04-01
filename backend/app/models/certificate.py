# Sertifikat modeli — kursni tugatgan foydalanuvchilarga PDF sertifikat
# UniqueConstraint(user_id, course_id) — har bir kurs uchun 1 ta sertifikat

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Certificate(Base):
    """Sertifikat jadvali — kursni 100% tugatgan foydalanuvchilarga."""

    __tablename__ = "certificates"

    __table_args__ = (
        # Bir foydalanuvchi + bir kurs = yagona sertifikat
        UniqueConstraint("user_id", "course_id", name="uq_certificate_user_course"),
    )

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

    # Qaysi kurs (FK → courses)
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Noyob sertifikat raqami: EDUUZ-2024-XXXXX formatida
    certificate_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    # Berilgan vaqt
    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # PDF fayl yo'li (media/certificates/XXXXX.pdf)
    pdf_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # Tegishli foydalanuvchi
    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="certificates",
    )

    # Tegishli kurs
    course: Mapped["Course"] = relationship(  # type: ignore
        "Course",
        back_populates="certificates",
    )

    def __repr__(self) -> str:
        return (
            f"<Certificate {self.certificate_number} "
            f"user={self.user_id} course={self.course_id}>"
        )
