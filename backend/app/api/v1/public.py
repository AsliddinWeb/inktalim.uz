# Ochiq (tokensiz) endpointlar — landing page uchun
# Hech qanday autentifikatsiya talab qilinmaydi

import uuid
from pydantic import BaseModel

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson

router = APIRouter()


class PublicCourseItem(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    thumbnail_url: str | None
    lessons_count: int = 0

    model_config = {"from_attributes": True}


@router.get("/courses", response_model=list[PublicCourseItem])
async def get_public_courses(
    db: AsyncSession = Depends(get_db),
) -> list[PublicCourseItem]:
    """Nashr qilingan kurslar ro'yxati — token talab qilinmaydi."""
    result = await db.execute(
        select(Course)
        .where(Course.is_published.is_(True))
        .order_by(Course.order.asc())
    )
    courses = result.scalars().all()

    items = []
    for course in courses:
        count_result = await db.execute(
            select(func.count()).where(
                Lesson.course_id == course.id,
                Lesson.is_published.is_(True),
            )
        )
        lessons_count = count_result.scalar_one()
        items.append(
            PublicCourseItem(
                id=course.id,
                title=course.title,
                description=course.description,
                thumbnail_url=course.thumbnail_url,
                lessons_count=lessons_count,
            )
        )

    return items
