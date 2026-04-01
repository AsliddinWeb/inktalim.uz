# Barcha modellarni bir joydan import qilish uchun
# Alembic autogenerate uchun hammasi shu yerda ko'rinishi kerak

from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.quiz import Quiz, Question, Choice
from app.models.quiz_attempt import QuizAttempt, AttemptAnswer
from app.models.certificate import Certificate

__all__ = [
    "User",
    "Course",
    "Lesson",
    "Progress",
    "Quiz",
    "Question",
    "Choice",
    "QuizAttempt",
    "AttemptAnswer",
    "Certificate",
]
