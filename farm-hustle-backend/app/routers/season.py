from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..db import get_db
from ..models import Season
from ..schemas import SeasonOut
from ..config import get_settings

router = APIRouter()


def get_or_create_current_season(db: Session):
    settings = get_settings()
    now = datetime.utcnow()
    s = (
        db.query(Season)
        .filter(Season.status == "active")
        .order_by(Season.id.desc())
        .first()
    )
    if s and s.ends_at > now:
        return s
    # create new
    starts = now
    ends = starts + timedelta(days=settings.SEASON_LENGTH_DAYS)
    s = Season(starts_at=starts, ends_at=ends, status="active")
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("", response_model=SeasonOut)
def season(db: Session = Depends(get_db)):
    settings = get_settings()
    s = get_or_create_current_season(db)
    # preview pool
    pool_pct = settings.PRIZE_POOL_PERCENT / 100.0 * s.net_revenue_usd
    pool_preview = (
        max(min(pool_pct, settings.PRIZE_POOL_CAP_USD), settings.PRIZE_POOL_MIN_USD)
        if s.net_revenue_usd > 0
        else settings.PRIZE_POOL_MIN_USD
    )
    return {
        "id": s.id,
        "starts_at": s.starts_at,
        "ends_at": s.ends_at,
        "status": s.status,
        "net_revenue_usd": s.net_revenue_usd,
        "prize_pool_preview_usd": round(pool_preview, 2),
        "cap_usd": settings.PRIZE_POOL_CAP_USD,
        "min_usd": settings.PRIZE_POOL_MIN_USD,
    }
