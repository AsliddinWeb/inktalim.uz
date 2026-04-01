# Barcha Pydantic schemalarini bir joydan import qilish
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse,
)
from app.schemas.lesson import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    LessonListResponse,
)
from app.schemas.progress import (
    ProgressCreate,
    ProgressUpdate,
    ProgressResponse,
    CourseProgressResponse,
)

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse", "UserListResponse",
    "CourseCreate", "CourseUpdate", "CourseResponse", "CourseListResponse",
    "LessonCreate", "LessonUpdate", "LessonResponse", "LessonListResponse",
    "ProgressCreate", "ProgressUpdate", "ProgressResponse", "CourseProgressResponse",
]
