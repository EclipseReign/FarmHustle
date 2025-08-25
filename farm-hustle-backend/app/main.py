from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .db import Base, engine

# ВАЖНО: поднимем модели до create_all(), чтобы SQLAlchemy видел все таблицы
from . import models  # noqa: F401

# Роуты импортируем после моделей
from .routers import auth, game, leaderboard, season, admin, progress

settings = get_settings()

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Farm Hustle Backend")

# CORS
origins = (
    [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]
    if settings.ALLOWED_ORIGINS
    else ["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Роуты
app.include_router(auth.router, prefix="")
app.include_router(game.router, prefix="/game", tags=["game"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(season.router, prefix="/season", tags=["season"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(progress.router, prefix="", tags=["progress"])

@app.get("/healthz")
def health():
    return {"ok": True}
