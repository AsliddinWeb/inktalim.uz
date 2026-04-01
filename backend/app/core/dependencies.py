# FastAPI Dependency Injection — joriy foydalanuvchini token orqali olish
# get_current_user: barcha autentifikatsiya talab qiluvchi endpointlar uchun
# get_current_admin: faqat adminlar uchun endpointlarda ishlatiladi

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import ACCESS_TOKEN_TYPE, decode_token
from app.database import get_db
from app.models.user import User

# Bearer token sxemasi — "Authorization: Bearer <token>" headerini o'qiydi
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Bearer tokendan joriy foydalanuvchini aniqlash.

    Xato hollari:
    - Token yo'q → 401
    - Token noto'g'ri yoki muddati o'tgan → 401
    - Token turi refresh → 401
    - Foydalanuvchi topilmadi → 401
    - Foydalanuvchi bloklangan → 403
    """
    # Token mavjudligini tekshirish
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kirish uchun token taqdim eting. Avval login qiling.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Tokenni dekodlash
    payload = decode_token(credentials.credentials)

    # Token turi tekshiruvi — refresh token ishlatib bo'lmaydi
    if payload.get("type") != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bu endpoint uchun access token taqdim eting.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Foydalanuvchi ID ni olish
    user_id_str: str | None = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz: foydalanuvchi ma'lumotlari topilmadi.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # UUID ga o'tkazish
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz: noto'g'ri foydalanuvchi ID.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # DB dan foydalanuvchini olish
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Foydalanuvchi topilmadi. Token eskirgan bo'lishi mumkin.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Bloklangan foydalanuvchi tekshiruvi
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hisobingiz bloklangan. Administrator bilan bog'laning.",
        )

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Faqat admin foydalanuvchilarga ruxsat berish.

    Agar is_admin=False bo'lsa → 403 Forbidden qaytaradi.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu amalni bajarish uchun admin huquqi talab qilinadi.",
        )
    return current_user
