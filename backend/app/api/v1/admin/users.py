# Admin — Foydalanuvchilar CRUD
# Faqat admin huquqiga ega foydalanuvchilar uchun
# GET ro'yxat (pagination + search), GET bitta, PUT yangilash, DELETE o'chirish

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserListResponse, UserResponse, UserUpdate

router = APIRouter()


@router.get(
    "",
    response_model=UserListResponse,
    summary="Barcha foydalanuvchilar ro'yxati",
)
async def list_users(
    skip: int = Query(0, ge=0, description="Nechta yozuvni o'tkazib yuborish"),
    limit: int = Query(20, ge=1, le=100, description="Bir sahifada nechta"),
    search: str | None = Query(None, description="Ism yoki email bo'yicha qidirish"),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> UserListResponse:
    """
    Barcha foydalanuvchilar ro'yxati.

    - Pagination: skip / limit
    - Qidiruv: email yoki to'liq ism bo'yicha (qisman moslik)
    - Yaratilgan vaqt bo'yicha teskari tartibda (yangilari birinchi)
    """
    # Asosiy so'rov
    query = select(User)

    # Qidiruv filtri (ILIKE — katta-kichik harfdan qat'i nazar)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                User.email.ilike(search_pattern),
                User.full_name.ilike(search_pattern),
                User.phone.ilike(search_pattern),
            )
        )

    # Jami sonni hisoblash (pagination uchun)
    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar_one()

    # Asosiy ma'lumotlarni olish
    query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    return UserListResponse(total=total, items=list(users))


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Bitta foydalanuvchi ma'lumotlari",
)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> User:
    """UUID bo'yicha bitta foydalanuvchi ma'lumotlarini olish."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Foydalanuvchi topilmadi (ID: {user_id}).",
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Foydalanuvchi ma'lumotlarini yangilash",
)
async def update_user(
    user_id: uuid.UUID,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
) -> User:
    """
    Foydalanuvchi ma'lumotlarini yangilash.

    Admin is_active ni ham o'zgartira oladi (bloklash/ochish).
    Telefon o'zgartirilsa noyoblik tekshiriladi.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Foydalanuvchi topilmadi (ID: {user_id}).",
        )

    # Telefon noyoblik tekshiruvi (o'zgartirilsa)
    if body.phone and body.phone != user.phone:
        existing_phone = await db.execute(
            select(User).where(
                User.phone == body.phone,
                User.id != user_id,
            )
        )
        if existing_phone.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{body.phone}' telefon raqami boshqa foydalanuvchiga tegishli.",
            )

    # Maydonlarni yangilash (faqat None bo'lmaganlar)
    update_data = body.model_dump(exclude_none=True, exclude={"password"})
    for field, value in update_data.items():
        setattr(user, field, value)

    # Parol yangilash (admin ham parol o'zgartira oladi)
    if body.password:
        from app.core.security import hash_password
        user.hashed_password = hash_password(body.password)

    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Foydalanuvchini o'chirish",
)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
) -> dict:
    """
    Foydalanuvchini o'chirish.

    - Topilmasa → 404
    - Admin o'zini o'chira olmaydi → 400
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Foydalanuvchi topilmadi (ID: {user_id}).",
        )

    # Admin o'zini o'chira olmaydi
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O'z hisobingizni o'chira olmaysiz.",
        )

    await db.delete(user)
    await db.flush()

    return {
        "message": f"'{user.full_name}' foydalanuvchisi muvaffaqiyatli o'chirildi."
    }
