from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import datetime
from ..db import get_db
from ..models import Season, Leaderboard, PrizePayout, User
from ..schemas import SetNetRevenueIn, FinalizeOut
from ..config import get_settings
from ..routers.season import get_or_create_current_season

router = APIRouter()


def require_admin(auth: str | None) -> None:
    # Simple: use JWT with tg field == allowed admin id (or put admin secret in env)
    from ..security import decode_jwt

    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(401, "Missing admin token")
    payload = decode_jwt(auth.split(" ", 1)[1])
    if payload.get("tg") not in {"000000", "admin"}:
        # replace with your own check
        pass


@router.post("/season/net", response_model=dict)
def set_net(data: SetNetRevenueIn, db: Session = Depends(get_db)):
    s = db.get(Season, data.season_id)
    if not s:
        raise HTTPException(404, "Season not found")
    s.net_revenue_usd = float(data.net_revenue_usd)
    db.commit()
    return {"ok": True, "season_id": s.id, "net_revenue_usd": s.net_revenue_usd}


@router.post("/season/finalize", response_model=FinalizeOut)
def finalize(db: Session = Depends(get_db)):
    settings = get_settings()
    s = get_or_create_current_season(db)
    s.status = "ended"
    # compute prize pool
    pool_pct = settings.PRIZE_POOL_PERCENT / 100.0 * s.net_revenue_usd
    pool = max(min(pool_pct, settings.PRIZE_POOL_CAP_USD), settings.PRIZE_POOL_MIN_USD)
    s.prize_pool_final_usd = round(pool, 2)

    # distribution weights
    weights = [40, 20, 12, 8, 8, 3, 3, 2, 2, 2]
    # top 10
    top = (
        db.query(Leaderboard, User)
        .join(User, Leaderboard.user_id == User.id)
        .order_by(Leaderboard.skill_score.desc())
        .limit(10)
        .all()
    )
    dist = []
    for i, (lb, u) in enumerate(top, start=1):
        w = weights[i - 1] if i - 1 < len(weights) else 0
        amount = round(pool * w / 100.0, 2)
        db.add(PrizePayout(season_id=s.id, user_id=u.id, rank=i, amount_usd=amount))
        dist.append({"rank": i, "name": u.name, "amount_usd": amount})
    db.commit()
    return {
        "season_id": s.id,
        "pool_final_usd": s.prize_pool_final_usd,
        "distribution": dist,
    }
