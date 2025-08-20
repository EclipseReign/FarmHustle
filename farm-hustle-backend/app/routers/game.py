from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from ..db import get_db
from ..models import User, UserBuilding, UserBoost, Leaderboard
from ..schemas import UpgradeIn, SnapshotOut
from ..economy import (
    CATALOG,
    upgrade_cost,
    current_income_per_sec,
    ensure_user_buildings,
    sets_active,
    skill_score_proxy,
)

router = APIRouter()


def require_user(db: Session, auth_header: str | None) -> User:
    from ..routers.auth import get_user_from_token

    return get_user_from_token(db, auth_header)


def accrue_offline(user: User):
    now = datetime.utcnow()
    elapsed = (now - user.last_tick_at).total_seconds()
    if elapsed < 0:
        elapsed = 0
    # cap offline accrual to 4 hours
    elapsed = min(elapsed, 4 * 3600)
    coins_gained = (user.cps_cached or 0) * elapsed
    user.coins += coins_gained
    user.last_tick_at = now


@router.post("/rotate")
def rotate(
    authorization: str | None = Header(default=None), db: Session = Depends(get_db)
):
    user = require_user(db, authorization)
    accrue_offline(user)
    ensure_user_buildings(db, user)
    ids = [b.building_id for b in user.buildings]
    random.shuffle(ids)
    targets = ids[:2]
    ends = datetime.utcnow() + timedelta(minutes=10)
    ub = UserBoost(
        user_id=user.id,
        label="Hot Zone",
        multiplier=3.0,
        ends_at=ends,
        targets={"ids": targets},
    )
    user.boosts_used += 1
    db.add(ub)
    user.cps_cached = current_income_per_sec(user)
    db.commit()
    return {"ok": True, "targets": targets, "ends_at": ends.isoformat()}


@router.post("/upgrade", response_model=SnapshotOut)
def upgrade(
    data: UpgradeIn,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    user = require_user(db, authorization)
    accrue_offline(user)
    ensure_user_buildings(db, user)
    bid = data.building_id
    ub = next((x for x in user.buildings if x.building_id == bid), None)
    if not ub:
        raise HTTPException(400, "Unknown building")
    cost = upgrade_cost(bid, ub.level)
    if user.coins < cost:
        raise HTTPException(400, "Not enough coins")
    user.coins -= cost
    ub.level += 1
    user.cps_cached = current_income_per_sec(user)

    # update leaderboard proxy
    sa = sets_active(user.buildings)
    score = skill_score_proxy(user.cps_cached, sa, user.boosts_used)
    lb = db.query(Leaderboard).filter_by(user_id=user.id).first()
    if not lb:
        lb = Leaderboard(user_id=user.id, skill_score=score)
        db.add(lb)
    else:
        lb.skill_score = max(lb.skill_score, score)
        lb.updated_at = datetime.utcnow()
    db.commit()

    # return snapshot
    from ..routers.auth import me as me_fn

    return me_fn(authorization, db)  # reuse serializer


@router.post("/prestige", response_model=SnapshotOut)
def prestige(
    authorization: str | None = Header(default=None), db: Session = Depends(get_db)
):
    user = require_user(db, authorization)
    accrue_offline(user)
    # Simple token award: if cps above threshold, +1 token (stub, replace with your curve)
    if user.cps_cached >= 25:
        user.prestige_tokens += 1
    # Reset early buildings
    for ub in user.buildings:
        ub.level = 1 if ub.building_id == "grain" else 0
    user.coins = 200
    user.boosts_used = 0
    db.query(UserBoost).filter_by(user_id=user.id).delete()
    user.cps_cached = current_income_per_sec(user)
    db.commit()
    from ..routers.auth import me as me_fn

    return me_fn(authorization, db)
