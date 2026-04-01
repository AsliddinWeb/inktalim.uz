# Fayl yuklash endpointlari
# POST /upload/thumbnail — faqat admin (kurs muqovasi)
# POST /upload/avatar   — har qanday login bo'lgan foydalanuvchi
# DELETE /upload/thumbnail/{filename} — faqat admin

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin, get_current_user
from app.core.file_handler import delete_file, save_file, validate_image
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


# ─── Javob schemalar ─────────────────────────────────────────────────────────

class UploadResponse(BaseModel):
    """Fayl yuklash muvaffaqiyatli bo'lgandagi javob."""
    url: str


class AvatarUploadResponse(BaseModel):
    """Avatar yuklash javobi — URL va yangilangan foydalanuvchi."""
    url: str
    user: UserResponse


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.post(
    "/thumbnail",
    response_model=UploadResponse,
    summary="Kurs muqovasini yuklash (faqat admin)",
)
async def upload_thumbnail(
    file: UploadFile = File(..., description="JPG/PNG/WEBP, maksimal 5MB"),
    _: User = Depends(get_current_admin),
) -> UploadResponse:
    """
    Kurs thumbnail rasmini yuklash.

    - Faqat adminlar uchun
    - Formatlar: jpg, jpeg, png, webp
    - Maksimal hajm: 5MB
    - Qaytaradi: { "url": "/media/thumbnails/uuid.jpg" }
    """
    await validate_image(file)
    url = await save_file(file, "thumbnails")
    return UploadResponse(url=url)


@router.post(
    "/avatar",
    response_model=AvatarUploadResponse,
    summary="Foydalanuvchi avatarini yuklash",
)
async def upload_avatar(
    file: UploadFile = File(..., description="JPG/PNG/WEBP, maksimal 5MB"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AvatarUploadResponse:
    """
    Foydalanuvchi profilining avatar rasmini yuklash.

    - Login bo'lgan har qanday foydalanuvchi uchun
    - Eski avatar avtomatik o'chiriladi (diskdan ham)
    - Foydalanuvchining avatar_url maydonini avtomatik yangilaydi
    - Qaytaradi: { "url": "/media/avatars/uuid.jpg", "user": {...} }
    """
    await validate_image(file)

    # Eski avatarni diskdan o'chirish
    if current_user.avatar_url and current_user.avatar_url.startswith("/media/"):
        delete_file(current_user.avatar_url)

    # Yangi avatarni saqlash
    url = await save_file(file, "avatars")

    # Foydalanuvchi yozuvini yangilash
    current_user.avatar_url = url
    db.add(current_user)
    await db.flush()
    await db.refresh(current_user)

    return AvatarUploadResponse(
        url=url,
        user=UserResponse.model_validate(current_user),
    )


@router.delete(
    "/thumbnail/{filename}",
    summary="Kurs muqovasini o'chirish (faqat admin)",
)
async def delete_thumbnail(
    filename: str,
    _: User = Depends(get_current_admin),
) -> dict:
    """
    Thumbnail rasmini diskdan o'chirish.

    - Faqat adminlar uchun
    - Fayl mavjud bo'lmasa ham 200 qaytaradi (idempotent)
    """
    delete_file(f"/media/thumbnails/{filename}")
    return {"message": "Rasm muvaffaqiyatli o'chirildi."}
