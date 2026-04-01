# Foydalanuvchi Pydantic schemalari — API kirish/chiqish validatsiyasi
# O'zbekiston telefon formati: +998XXXXXXXXX (regex bilan tekshiriladi)

import re
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


# Telefon raqami validatsiya regex — O'zbekiston formati
UZ_PHONE_PATTERN = re.compile(r"^\+998[0-9]{9}$")


class UserBase(BaseModel):
    """Foydalanuvchi uchun umumiy maydonlar."""
    full_name: str = Field(..., min_length=2, max_length=255, description="To'liq ism")
    email: EmailStr = Field(..., description="Email manzil")
    phone: str = Field(..., description="Telefon: +998XXXXXXXXX")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """O'zbekiston telefon formatini tekshirish."""
        if not UZ_PHONE_PATTERN.match(v):
            raise ValueError(
                "Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak. "
                "Masalan: +998901234567"
            )
        return v


class UserCreate(UserBase):
    """Yangi foydalanuvchi yaratish uchun schema."""
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Parol (kamida 8 ta belgi)",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Parol kuchli ekanligini tekshirish."""
        if not any(c.isdigit() for c in v):
            raise ValueError("Parolda kamida bitta raqam bo'lishi kerak")
        return v


class UserUpdate(BaseModel):
    """Foydalanuvchi ma'lumotlarini yangilash uchun schema (barcha maydonlar ixtiyoriy)."""
    full_name: str | None = Field(None, min_length=2, max_length=255)
    phone: str | None = None
    avatar_url: str | None = Field(None, max_length=500)
    password: str | None = Field(None, min_length=8, max_length=128)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is not None and not UZ_PHONE_PATTERN.match(v):
            raise ValueError("Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak")
        return v


class UserResponse(BaseModel):
    """API javobida qaytariladigan foydalanuvchi ma'lumotlari (parolsiz)."""
    id: uuid.UUID
    full_name: str
    email: str
    phone: str
    is_active: bool
    is_admin: bool
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime

    # SQLAlchemy obyektidan o'qishga ruxsat
    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    """Foydalanuvchilar ro'yxati uchun wrapper."""
    total: int
    items: list[UserResponse]
