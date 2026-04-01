# FastAPI ilovasining kirish nuqtasi
# CORS, router, StaticFiles va startup/shutdown eventlari shu yerda sozlanadi

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import settings


def _ensure_media_dirs() -> None:
    """
    Media papkalarini yaratish — ilova ishga tushganda chaqiriladi.
    Docker volume mavjud bo'lsa ham, ichki papkalar bo'lmashi mumkin.
    """
    for folder in ("thumbnails", "avatars", "certificates"):
        path = Path(settings.MEDIA_DIR) / folder
        path.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ilova ishga tushganda va to'xtatilganda bajariladigan ishlar."""
    # Ishga tushish — media papkalarini yaratish
    _ensure_media_dirs()
    print(f"Mini Udemy backend ishga tushdi — muhit: {settings.ENVIRONMENT}")
    print(f"Media papkasi: {Path(settings.MEDIA_DIR).resolve()}")
    yield
    # To'xtatish
    print("Mini Udemy backend to'xtatildi.")


# FastAPI ilovasi
app = FastAPI(
    title="Mini Udemy API",
    description="Online kurs platformasi uchun REST API",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc UI
    lifespan=lifespan,
)

# CORS sozlamalari — vergul bilan ajratilgan ALLOWED_ORIGINS dan o'qiladi
_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,              # Cookie va Auth header ruxsat
    allow_methods=["*"],                 # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],                 # Authorization, Content-Type va b.
)

# Statik fayllar — yuklangan rasm va medialar
# /media/thumbnails/xxx.jpg → media/thumbnails/xxx.jpg (diskdan)
app.mount(
    "/media",
    StaticFiles(directory=settings.MEDIA_DIR),
    name="media",
)


# Asosiy health-check endpoint
@app.get("/", tags=["Health"])
async def root():
    """API ishlayotganini tekshirish uchun."""
    return {
        "status": "ok",
        "message": "Mini Udemy API ishlayapti",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Docker healthcheck uchun endpoint."""
    return {"status": "healthy"}


# Barcha API v1 routerlarini ulanish — /api/v1/... prefiksi bilan
app.include_router(api_router, prefix="/api/v1")
