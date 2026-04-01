# Xavfsizlik moduli — JWT token yaratish va bcrypt parol xeshlash
# Access token: 30 daqiqa | Refresh token: 7 kun

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# Bcrypt parol xeshlash konteksti
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token turi konstantalari
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def hash_password(password: str) -> str:
    """Ochiq matn parolni bcrypt bilan xeshlash."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiritilgan parolni xeshlangan parol bilan solishtirish."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    JWT access token yaratish.

    Amal qilish muddati: 30 daqiqa (sozlamadan olinadi).
    data ichida odatda: {"sub": user_id, "email": email}
    """
    to_encode = data.copy()

    # Muddatni hisoblash
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({
        "exp": expire,
        "type": ACCESS_TOKEN_TYPE,
    })

    # Token imzolash
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict[str, Any]) -> str:
    """
    JWT refresh token yaratish.

    Amal qilish muddati: 7 kun.
    Yangi access token olish uchun ishlatiladi.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({
        "exp": expire,
        "type": REFRESH_TOKEN_TYPE,
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """
    JWT tokenni dekodlash va tasdiqlash.

    Xato hollari:
    - Token muddati o'tgan → 401
    - Token noto'g'ri → 401
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz yoki muddati o'tgan. Qayta login qiling.",
            headers={"WWW-Authenticate": "Bearer"},
        )
