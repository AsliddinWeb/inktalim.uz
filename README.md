# InkTalim.Uz — Online Ta'lim Platformasi

Online kurs platformasi. Foydalanuvchilar kurs ko'radi va progressini kuzatadi; adminlar kurs, dars va foydalanuvchilarni boshqaradi.

---

## Texnologiyalar

| Qatlam     | Stack |
|------------|-------|
| Backend    | FastAPI, SQLAlchemy (async), Alembic, PostgreSQL, python-jose, passlib |
| Frontend   | Vue 3, Vite, Tailwind CSS v3, Pinia, Vue Router 4, Axios, VeeValidate + Yup, Lucide |
| Infratuzilma | Docker, Docker Compose, Nginx |

---

## Tezkor ishga tushirish

### 1. Loyihani klonlash

```bash
git clone <repo-url>
cd MiniUdemyMagistr/project
```

### 2. `.env` faylini sozlash

```bash
cp .env.example .env
```

`.env` ichidagi qiymatlarni to'ldiring:

```env
POSTGRES_DB=inktalim
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@db:5432/inktalim
SECRET_KEY=your-very-secret-key-at-least-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Docker bilan ishga tushirish

```bash
docker compose up --build
```

| Servis   | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/v1 |
| Swagger docs | http://localhost:8000/docs |

### 4. Migratsiyalarni qo'llash

Birinchi ishga tushirishda backend avtomatik migratsiya qiladi. Agar qo'lda bajarmоqchi bo'lsangiz:

```bash
docker compose exec backend alembic upgrade head
```

### 5. Admin foydalanuvchi yaratish

```bash
docker compose exec backend python -c "
import asyncio
from app.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import hash_password
import uuid

async def create_admin():
    async with AsyncSessionLocal() as db:
        admin = User(
            id=uuid.uuid4(),
            email='admin@example.com',
            hashed_password=hash_password('admin123456'),
            full_name='Super Admin',
            is_admin=True,
            is_active=True,
        )
        db.add(admin)
        await db.commit()
        print('Admin yaratildi!')

asyncio.run(create_admin())
"
```

---

## Loyiha tuzilmasi

```
project/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── admin/        # Kurslar, darslar, foydalanuvchilar CRUD
│   │   │   ├── student/      # Kurs ko'rish, progress
│   │   │   └── auth.py       # JWT auth (register/login/refresh)
│   │   ├── core/             # Security, dependencies
│   │   ├── models/           # SQLAlchemy modellari
│   │   └── main.py
│   ├── alembic/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/              # Axios chaqiruvlari
│   │   ├── components/
│   │   │   ├── admin/        # StatCard, CourseForm, LessonForm
│   │   │   ├── student/      # CourseCard, LessonItem, ProgressCard
│   │   │   └── ui/           # AppButton, AppInput, AppModal, AppTable ...
│   │   ├── layouts/          # AuthLayout, StudentLayout, AdminLayout
│   │   ├── router/
│   │   ├── stores/           # Pinia: auth, theme, courses, progress, admin
│   │   └── views/
│   │       ├── admin/        # Dashboard, Courses, CourseDetail, Users, Profile
│   │       ├── auth/         # Login, Register
│   │       └── student/      # Dashboard, Courses, Lesson, Progress, Profile
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml
```

---

## API endpointlari

### Auth
| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/api/v1/auth/register` | Ro'yxatdan o'tish |
| POST | `/api/v1/auth/login` | Kirish (email yoki telefon) |
| GET  | `/api/v1/auth/me` | Profilni olish |
| PUT  | `/api/v1/auth/me` | Profilni yangilash |
| POST | `/api/v1/auth/refresh` | Token yangilash |
| POST | `/api/v1/auth/change-password` | Parol o'zgartirish |

### Admin (faqat `is_admin=true`)
| Method | URL | Tavsif |
|--------|-----|--------|
| GET/POST | `/api/v1/admin/courses` | Kurslar ro'yxati / Yangi kurs |
| PUT/DELETE | `/api/v1/admin/courses/{id}` | Kursni yangilash / o'chirish |
| PATCH | `/api/v1/admin/courses/{id}/publish` | Nashr holatini almashtirish |
| PUT | `/api/v1/admin/courses/reorder` | Tartibni o'zgartirish |
| GET/POST | `/api/v1/admin/courses/{id}/lessons` | Darslar |
| PUT/DELETE | `/api/v1/admin/courses/{id}/lessons/{lid}` | Darsni yangilash/o'chirish |
| GET | `/api/v1/admin/users` | Foydalanuvchilar ro'yxati |
| PUT/DELETE | `/api/v1/admin/users/{id}` | Foydalanuvchini boshqarish |

### Student
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/v1/student/courses` | Kurslar (progress bilan) |
| GET | `/api/v1/student/courses/{id}` | Kurs detail |
| GET | `/api/v1/student/courses/{id}/lessons/{lid}` | Dars (progress avtomatik yaratiladi) |
| POST/DELETE | `/api/v1/student/progress/lessons/{lid}/complete` | Bajarildi / Bekor |
| GET | `/api/v1/student/progress` | Barcha progress |

---

## Rivojlantirish (development)

Backend va frontendni alohida ishga tushirish:

```bash
# Backend (virtual environment bilan)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

> Frontend `http://localhost:5173` da, backend `http://localhost:8000` da ishlaydi.

---

## Dark/Light rejim

Foydalanuvchi interfeysi avtomatik tizim rangiga moslanadi. Yuqori o'ng burchakdagi quyosh/oy tugmasi orqali qo'lda ham almashtirish mumkin. Tanlov `localStorage` da saqlanadi.
