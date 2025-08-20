from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .db import Base, engine
from .routers import auth, game, leaderboard, season, admin

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Farm Hustle Backend")

origins = (
    [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]
    if settings.ALLOWED_ORIGINS
    else [""]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=[""],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router, prefix="")
app.include_router(game.router, prefix="/game", tags=["game"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(season.router, prefix="/season", tags=["season"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/healthz")
def health():
    return {"ok": True}
