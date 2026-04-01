# Auth endpointlari — ro'yxatdan o'tish, kirish, token yangilash va profil
# Barcha xato xabarlari o'zbek tilida

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.security import (
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


# ─── Yordamchi schemalar ─────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    """Login uchun — email yoki telefon bilan kirish imkoniyati."""
    login: str = Field(
        ...,
        description="Email manzil yoki telefon raqami (+998XXXXXXXXX)",
    )
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Login / refresh javobida qaytariladigan tokenlar."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """Refresh token bilan yangi access token olish."""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Parol o'zgartirish uchun schema."""
    old_password: str = Field(..., min_length=1, description="Hozirgi parol")
    new_password: str = Field(..., min_length=8, description="Yangi parol (kamida 8 belgi)")


# ─── Yordamchi funksiyalar ───────────────────────────────────────────────────

def _build_tokens(user: User) -> TokenResponse:
    """Foydalanuvchi uchun access va refresh token yaratish."""
    token_data = {"sub": str(user.id), "email": user.email}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi foydalanuvchi ro'yxatdan o'tkazish",
)
async def register(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Yangi student ro'yxatdan o'tkazish.

    - Email allaqachon mavjud bo'lsa → 400
    - Telefon allaqachon mavjud bo'lsa → 400
    - Muvaffaqiyatli → 201, UserResponse
    """
    # Email noyobligini tekshirish
    existing_email = await db.execute(
        select(User).where(User.email == body.email)
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{body.email}' email manzili allaqachon ro'yxatdan o'tgan.",
        )

    # Telefon noyobligini tekshirish
    existing_phone = await db.execute(
        select(User).where(User.phone == body.phone)
    )
    if existing_phone.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{body.phone}' telefon raqami allaqachon ro'yxatdan o'tgan.",
        )

    # Yangi foydalanuvchi yaratish (is_admin=False — faqat student)
    new_user = User(
        full_name=body.full_name,
        email=body.email,
        phone=body.phone,
        hashed_password=hash_password(body.password),
        is_active=True,
        is_admin=False,  # Register orqali admin bo'lib bo'lmaydi
    )
    db.add(new_user)
    await db.flush()  # ID olish uchun flush (commit keyinroq get_db da)
    await db.refresh(new_user)
    return new_user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Tizimga kirish (email yoki telefon bilan)",
)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Email yoki telefon raqami orqali kirish.

    - Foydalanuvchi topilmasa → 401
    - Parol noto'g'ri → 401
    - Hisob bloklangan → 403
    - Muvaffaqiyatli → access_token + refresh_token
    """
    # Email yoki telefon bo'yicha qidirish
    result = await db.execute(
        select(User).where(
            or_(
                User.email == body.login,
                User.phone == body.login,
            )
        )
    )
    user = result.scalar_one_or_none()

    # Foydalanuvchi topilmadi yoki parol noto'g'ri — bir xil xabar (xavfsizlik uchun)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parol noto'g'ri. Qaytadan urinib ko'ring.",
        )

    # Bloklangan hisob tekshiruvi
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hisobingiz bloklangan. Administrator bilan bog'laning.",
        )

    return _build_tokens(user)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Joriy foydalanuvchi ma'lumotlari",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    """Token orqali joriy foydalanuvchi profilini olish."""
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Profilni yangilash",
)
async def update_me(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Joriy foydalanuvchi profilini yangilash.

    Yangilanishi mumkin: full_name, phone, avatar_url.
    Parol alohida /change-password orqali o'zgartiriladi.
    """
    # Telefon o'zgartirilsa — noyobligini tekshirish
    if body.phone and body.phone != current_user.phone:
        existing = await db.execute(
            select(User).where(
                User.phone == body.phone,
                User.id != current_user.id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{body.phone}' telefon raqami boshqa foydalanuvchiga tegishli.",
            )

    # Maydonlarni yangilash (faqat None bo'lmaganlar)
    update_data = body.model_dump(exclude_none=True, exclude={"password"})
    for field, value in update_data.items():
        setattr(current_user, field, value)

    # Parol yangilash (agar berilgan bo'lsa)
    if body.password:
        current_user.hashed_password = hash_password(body.password)

    db.add(current_user)
    await db.flush()
    await db.refresh(current_user)
    return current_user


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Yangi access token olish",
)
async def refresh_token(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Refresh token orqali yangi access token olish.

    - Token yaroqsiz yoki muddati o'tgan → 401
    - Token turi 'refresh' emas → 401
    - Foydalanuvchi topilmasa → 401
    """
    # Tokenni tekshirish
    payload = decode_token(body.refresh_token)

    # Token turi tekshiruvi
    if payload.get("type") != REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token taqdim eting (access token emas).",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Foydalanuvchini olish
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz.",
        )

    result = await db.execute(
        select(User).where(User.id == uuid.UUID(user_id_str))
    )
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Foydalanuvchi topilmadi yoki hisob bloklangan.",
        )

    return _build_tokens(user)


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Parol o'zgartirish",
)
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Joriy parolni tekshirib yangi parol o'rnatish.

    - Eski parol noto'g'ri → 400
    - Yangi parol eski parol bilan bir xil → 400
    """
    # Eski parolni tekshirish
    if not verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Joriy parol noto'g'ri kiritildi.",
        )

    # Yangi parol eski parol bilan bir xil bo'lmasligi kerak
    if verify_password(body.new_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Yangi parol joriy paroldan farq qilishi kerak.",
        )

    # Yangi parolni saqlash
    current_user.hashed_password = hash_password(body.new_password)
    db.add(current_user)
    await db.flush()

    return {"message": "Parol muvaffaqiyatli o'zgartirildi."}
