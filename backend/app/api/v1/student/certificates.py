# Student — Sertifikat API
# Kursni 100% tugatgandan so'ng sertifikat olish va yuklab olish

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.certificate_generator import generate_certificate, generate_certificate_number
from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.certificate import Certificate
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.user import User
from app.schemas.certificate import CertificateListItem, CertificateResponse

router = APIRouter()

# Media papkasi (settings'dan ham olinishi mumkin, soddalik uchun to'g'ridan)
MEDIA_DIR = os.environ.get("MEDIA_DIR", "media")
CERT_DIR  = os.path.join(MEDIA_DIR, "certificates")


def _make_download_url(certificate_number: str) -> str:
    """Yuklab olish URL sini shakllantirish."""
    return f"/api/v1/student/certificates/download/{certificate_number}"


async def _check_course_completion(
    course_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession,
) -> bool:
    """Kurs 100% tugallanganligini tekshirish."""
    # Nashr qilingan darslar soni
    total_result = await db.execute(
        select(func.count()).where(
            Lesson.course_id == course_id,
            Lesson.is_published.is_(True),
        )
    )
    total = total_result.scalar_one()

    if total == 0:
        return False

    # Tugatilgan darslar soni
    completed_result = await db.execute(
        select(func.count()).where(
            Progress.course_id == course_id,
            Progress.user_id == user_id,
            Progress.is_completed.is_(True),
        )
    )
    completed = completed_result.scalar_one()

    return completed >= total


@router.get(
    "/courses/{course_id}/certificate",
    response_model=CertificateResponse,
    summary="Kurs uchun sertifikat olish yoki mavjudini qaytarish",
)
async def get_or_create_certificate(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CertificateResponse:
    """
    Kurs 100% tugallangan bo'lsa sertifikat yaratadi yoki mavjudini qaytaradi.

    - Kurs topilmasa → 404
    - Kurs 100% tugatilmagan → 403
    - Allaqachon sertifikat bor → mavjudini qaytaradi
    - Yangi → PDF generatsiya qilib saqlaydi
    """
    # Kursni tekshirish
    course_result = await db.execute(
        select(Course).where(
            Course.id == course_id,
            Course.is_published.is_(True),
        )
    )
    course = course_result.scalar_one_or_none()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs topilmadi",
        )

    # Kurs tugallanganligini tekshirish
    is_complete = await _check_course_completion(course_id, current_user.id, db)
    if not is_complete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kursni to'liq tugatmadingiz. Barcha darslarni tugating.",
        )

    # Mavjud sertifikatni tekshirish
    cert_result = await db.execute(
        select(Certificate).where(
            Certificate.user_id == current_user.id,
            Certificate.course_id == course_id,
        )
    )
    existing = cert_result.scalar_one_or_none()

    if existing:
        return CertificateResponse(
            certificate_number=existing.certificate_number,
            issued_at=existing.issued_at,
            download_url=_make_download_url(existing.certificate_number),
            course_id=course.id,
            course_title=course.title,
        )

    # Yangi sertifikat raqami
    cert_number = generate_certificate_number()

    # Noyobligini ta'minlash (kam ehtimolli, lekin xavfsiz)
    for _ in range(5):
        existing_num = await db.execute(
            select(Certificate).where(Certificate.certificate_number == cert_number)
        )
        if not existing_num.scalar_one_or_none():
            break
        cert_number = generate_certificate_number()

    # PDF fayl yo'li
    pdf_filename = f"{cert_number}.pdf"
    pdf_path = os.path.join(CERT_DIR, pdf_filename)

    # PDF generatsiya
    generate_certificate(
        full_name=current_user.full_name,
        course_title=course.title,
        certificate_number=cert_number,
        issued_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
        output_path=pdf_path,
    )

    # DB ga saqlash
    cert = Certificate(
        user_id=current_user.id,
        course_id=course_id,
        certificate_number=cert_number,
        pdf_path=pdf_path,
    )
    db.add(cert)
    await db.commit()
    await db.refresh(cert)

    return CertificateResponse(
        certificate_number=cert.certificate_number,
        issued_at=cert.issued_at,
        download_url=_make_download_url(cert.certificate_number),
        course_id=course.id,
        course_title=course.title,
    )


@router.get(
    "",
    response_model=list[CertificateListItem],
    summary="Foydalanuvchining barcha sertifikatlari",
)
async def list_certificates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CertificateListItem]:
    """Joriy foydalanuvchining barcha sertifikatlari ro'yxati."""
    result = await db.execute(
        select(Certificate, Course)
        .join(Course, Certificate.course_id == Course.id)
        .where(Certificate.user_id == current_user.id)
        .order_by(Certificate.issued_at.desc())
    )
    rows = result.all()

    return [
        CertificateListItem(
            certificate_number=cert.certificate_number,
            course_id=course.id,
            course_title=course.title,
            course_thumbnail=course.thumbnail_url,
            issued_at=cert.issued_at,
            download_url=_make_download_url(cert.certificate_number),
        )
        for cert, course in rows
    ]


@router.get(
    "/download/{certificate_number}",
    summary="Sertifikat PDF ni yuklab olish",
    response_class=FileResponse,
)
async def download_certificate(
    certificate_number: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FileResponse:
    """
    Sertifikat raqami bo'yicha PDF fayl qaytaradi.
    Faqat o'z sertifikatini yuklab olish mumkin.
    """
    result = await db.execute(
        select(Certificate).where(
            Certificate.certificate_number == certificate_number,
        )
    )
    cert = result.scalar_one_or_none()

    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sertifikat topilmadi",
        )

    if cert.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu sertifikat sizga tegishli emas",
        )

    if not Path(cert.pdf_path).exists():
        # PDF yo'q bo'lsa — qayta generatsiya
        course_result = await db.execute(
            select(Course).where(Course.id == cert.course_id)
        )
        course = course_result.scalar_one_or_none()
        if course:
            generate_certificate(
                full_name=current_user.full_name,
                course_title=course.title,
                certificate_number=cert.certificate_number,
                issued_at=cert.issued_at,
                output_path=cert.pdf_path,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sertifikat fayli topilmadi",
            )

    return FileResponse(
        path=cert.pdf_path,
        media_type="application/pdf",
        filename=f"EduUz-Sertifikat-{certificate_number}.pdf",
        headers={"Content-Disposition": f'attachment; filename="EduUz-Sertifikat-{certificate_number}.pdf"'},
    )
