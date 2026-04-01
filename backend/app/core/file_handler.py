# Fayl boshqaruvi — rasm yuklash, saqlash va o'chirish
# Faqat rasm formatlari qabul qilinadi: jpg, jpeg, png, webp
# Maksimal hajm: 5MB

import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.config import settings

# Ruxsat etilgan MIME turlari va kengaytmalar
ALLOWED_CONTENT_TYPES: set[str] = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
}
ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".webp"}

# Maksimal fayl hajmi — 5 MB
MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5_242_880 bayt


async def validate_image(file: UploadFile) -> bytes:
    """
    Yuklangan faylni tekshirish:
    - Fayl turi: faqat jpg, jpeg, png, webp
    - Fayl hajmi: 5MB dan oshmasligi kerak

    Muvaffaqiyatli tekshiruvdan so'ng fayl kontentini (bytes) qaytaradi,
    shunda qayta o'qish shart bo'lmaydi.

    Xato hollarida HTTPException 400 qaytaradi.
    """
    # Kengaytma tekshiruvi
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Faqat JPG, JPEG, PNG, WEBP formatlar qabul qilinadi.",
        )

    # Content-Type tekshiruvi
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Faqat JPG, JPEG, PNG, WEBP formatlar qabul qilinadi.",
        )

    # Faylni o'qish va hajmini tekshirish
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fayl hajmi 5MB dan oshmasligi kerak.",
        )

    # Faylni boshiga qaytarish (keyingi o'qishlar uchun)
    await file.seek(0)
    return content


async def save_file(file: UploadFile, folder: str) -> str:
    """
    Faylni media papkasiga UUID nom bilan saqlash.

    Args:
        file:   FastAPI UploadFile obyekti
        folder: "thumbnails" yoki "avatars"

    Returns:
        Fayl URL yo'li: "/media/thumbnails/uuid.jpg" formatida

    Eslatma:
        validate_image() dan keyin chaqirilishi kerak.
    """
    # Kengaytmani saqlab, UUID nom yaratish
    ext = Path(file.filename or "file").suffix.lower()
    filename = f"{uuid.uuid4()}{ext}"

    # Papkani yaratish (mavjud bo'lsa ham xato bermaydi)
    dir_path = Path(settings.MEDIA_DIR) / folder
    dir_path.mkdir(parents=True, exist_ok=True)

    # Faylni o'qib, diskka yozish
    content = await file.read()
    file_path = dir_path / filename
    file_path.write_bytes(content)

    # URL yo'lini qaytarish — frontend uchun
    return f"/media/{folder}/{filename}"


def delete_file(url_path: str) -> None:
    """
    Faylni diskdan o'chirish.

    Args:
        url_path: "/media/thumbnails/uuid.jpg" ko'rinishidagi URL yo'l

    Fayl mavjud bo'lmasa, jimgina o'tkazib yuboriladi.
    """
    if not url_path:
        return

    # URL yo'ldan fayl tizimi yo'lini olish
    # "/media/thumbnails/uuid.jpg" → "thumbnails/uuid.jpg"
    parts = url_path.split("/media/", 1)
    if len(parts) < 2 or not parts[1]:
        return

    full_path = Path(settings.MEDIA_DIR) / parts[1]
    try:
        if full_path.exists():
            full_path.unlink()
    except OSError:
        # O'chirishda xatolik — jimgina o'tkazib yuboramiz
        pass
