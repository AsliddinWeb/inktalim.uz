# Student — Kurslar API
# Faqat nashr qilingan kurslarni ko'rish, progress ma'lumotlari bilan
# Ro'yxatdan o'tgan har qanday foydalanuvchi uchun (student yoki admin)

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import Progress
from app.models.user import User

router = APIRouter()


# ─── Javob schemalari ─────────────────────────────────────────────────────────

class LessonBriefResponse(BaseModel):
    """Kurs detail sahifasida har bir dars uchun qisqa ma'lumot."""
    id: uuid.UUID
    title: str
    order: int
    duration_minutes: int | None
    video_url: str | None
    is_completed: bool = False
    module_id: uuid.UUID | None = None

    model_config = {"from_attributes": True}


class ModuleBriefResponse(BaseModel):
    """Kurs detail sahifasida har bir modul uchun javob."""
    id: uuid.UUID
    title: str
    description: str | None
    order: int
    is_published: bool
    lessons: list[LessonBriefResponse] = []

    model_config = {"from_attributes": True}


class CourseListItemResponse(BaseModel):
    """Kurslar ro'yxatida har bir kurs uchun javob."""
    id: uuid.UUID
    title: str
    description: str
    thumbnail_url: str | None
    order: int
    lessons_count: int = 0
    completed_lessons: int = 0
    progress_percent: float = 0.0
    is_enrolled: bool = False       # Birorta darsni ochgan bo'lsa True

    model_config = {"from_attributes": True}


class CourseDetailResponse(BaseModel):
    """Kurs detail sahifasi uchun to'liq javob."""
    id: uuid.UUID
    title: str
    description: str
    thumbnail_url: str | None
    order: int
    lessons_count: int = 0
    completed_lessons: int = 0
    progress_percent: float = 0.0
    is_enrolled: bool = False
    modules: list[ModuleBriefResponse] = []
    lessons: list[LessonBriefResponse] = []   # modulsiz darslar

    model_config = {"from_attributes": True}


# ─── Yordamchi funksiyalar ────────────────────────────────────────────────────

def _calc_percent(completed: int, total: int) -> float:
    """Progress foizini hisoblash. Total=0 bo'lsa 0.0 qaytaradi."""
    if total == 0:
        return 0.0
    return round(completed / total * 100, 1)


async def _get_published_course_or_404(
    course_id: uuid.UUID,
    db: AsyncSession,
) -> Course:
    """Nashr qilingan kursni olish, topilmasa 404."""
    result = await db.execute(
        select(Course).where(
            Course.id == course_id,
            Course.is_published == True,  # noqa: E712
        )
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs topilmadi yoki hali nashr qilinmagan.",
        )
    return course


async def _get_course_stats(
    course_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession,
) -> dict:
    """
    Bitta kurs uchun statistikani hisoblash:
    - Jami nashr qilingan darslar soni
    - Foydalanuvchi tomonidan tugatilgan darslar soni
    - Progress foizi
    - Ro'yxatdan o'tganmi (enrolled)
    """
    # Nashr qilingan darslar soni
    total_result = await db.execute(
        select(func.count()).where(
            Lesson.course_id == course_id,
            Lesson.is_published == True,  # noqa: E712
        )
    )
    total = total_result.scalar_one()

    # Foydalanuvchi tugatgan darslar soni
    completed_result = await db.execute(
        select(func.count()).where(
            Progress.course_id == course_id,
            Progress.user_id == user_id,
            Progress.is_completed == True,  # noqa: E712
        )
    )
    completed = completed_result.scalar_one()

    # Boshlangan (enrolled) — birorta progress yozuvi mavjud bo'lsa
    enrolled_result = await db.execute(
        select(func.count()).where(
            Progress.course_id == course_id,
            Progress.user_id == user_id,
        )
    )
    is_enrolled = enrolled_result.scalar_one() > 0

    return {
        "lessons_count": total,
        "completed_lessons": completed,
        "progress_percent": _calc_percent(completed, total),
        "is_enrolled": is_enrolled,
    }


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=list[CourseListItemResponse],
    summary="Nashr qilingan kurslar ro'yxati",
)
async def list_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CourseListItemResponse]:
    """
    Barcha nashr qilingan kurslarni ko'rish.

    Har bir kurs uchun:
    - Asosiy ma'lumotlar (title, description, thumbnail)
    - lessons_count — nashr qilingan darslar soni
    - completed_lessons — bu user tugatgan darslar soni
    - progress_percent — tugatilganlik foizi
    - is_enrolled — user bu kursni boshlagan yoki yo'q
    """
    # Nashr qilingan kurslar, tartib bo'yicha
    result = await db.execute(
        select(Course)
        .where(Course.is_published == True)  # noqa: E712
        .order_by(Course.order.asc(), Course.created_at.asc())
    )
    courses = result.scalars().all()

    # Har bir kurs uchun statistika hisoblash
    items = []
    for course in courses:
        stats = await _get_course_stats(course.id, current_user.id, db)
        items.append(
            CourseListItemResponse(
                id=course.id,
                title=course.title,
                description=course.description,
                thumbnail_url=course.thumbnail_url,
                order=course.order,
                **stats,
            )
        )

    return items


@router.get(
    "/{course_id}",
    response_model=CourseDetailResponse,
    summary="Kurs detail sahifasi",
)
async def get_course_detail(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CourseDetailResponse:
    """
    Kurs haqida to'liq ma'lumot va nashr qilingan darslari ro'yxati.

    Har bir dars uchun is_completed — joriy foydalanuvchi tugatganmi.
    Faqat nashr qilingan darslar ko'rinadi.
    """
    course = await _get_published_course_or_404(course_id, db)

    # Barcha nashr qilingan darslar
    lessons_result = await db.execute(
        select(Lesson)
        .where(Lesson.course_id == course_id, Lesson.is_published == True)  # noqa: E712
        .order_by(Lesson.order.asc())
    )
    all_lessons = lessons_result.scalars().all()

    # Progress map
    lesson_ids = [l.id for l in all_lessons]
    if lesson_ids:
        progress_result = await db.execute(
            select(Progress).where(
                Progress.user_id == current_user.id,
                Progress.lesson_id.in_(lesson_ids),
            )
        )
        progress_map: dict[uuid.UUID, Progress] = {
            p.lesson_id: p for p in progress_result.scalars().all()
        }
    else:
        progress_map = {}

    def make_lesson(lesson: Lesson) -> LessonBriefResponse:
        prog = progress_map.get(lesson.id)
        return LessonBriefResponse(
            id=lesson.id,
            title=lesson.title,
            order=lesson.order,
            duration_minutes=lesson.duration_minutes,
            video_url=lesson.video_url,
            module_id=lesson.module_id,
            is_completed=prog.is_completed if prog else False,
        )

    # Modullar (nashr qilingan)
    modules_result = await db.execute(
        select(Module)
        .where(Module.course_id == course_id, Module.is_published == True)  # noqa: E712
        .order_by(Module.order.asc())
    )
    modules = modules_result.scalars().all()

    module_responses: list[ModuleBriefResponse] = []
    module_ids = {m.id for m in modules}
    for mod in modules:
        mod_lessons = [l for l in all_lessons if l.module_id == mod.id]
        module_responses.append(ModuleBriefResponse(
            id=mod.id,
            title=mod.title,
            description=mod.description,
            order=mod.order,
            is_published=mod.is_published,
            lessons=[make_lesson(l) for l in mod_lessons],
        ))

    # Modulsiz darslar (module_id == None yoki modulga tegishli emas)
    standalone_lessons = [l for l in all_lessons if l.module_id not in module_ids]

    stats = await _get_course_stats(course_id, current_user.id, db)

    return CourseDetailResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        thumbnail_url=course.thumbnail_url,
        order=course.order,
        modules=module_responses,
        lessons=[make_lesson(l) for l in standalone_lessons],
        **stats,
    )
