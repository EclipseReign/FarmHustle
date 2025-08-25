from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from ..db import get_db
from ..models import User, DailyClaim, Referral
from ..config import get_settings
from .auth import get_user_from_token

router = APIRouter(tags=["progress"])

@router.post("/progress/daily/claim")
def daily_claim(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    user = get_user_from_token(db, authorization)
    today = date.today()
    exists = db.query(DailyClaim).filter_by(user_id=user.id, claimed_on=today).first()
    if exists:
        raise HTTPException(status_code=400, detail="Already claimed today")
    user.coins += 200
    db.add(DailyClaim(user_id=user.id, claimed_on=today))
    db.commit()
    return {"ok": True, "coins_added": 200, "claimed_on": today.isoformat()}

@router.get("/progress/invite_link")
def invite_link(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    user = get_user_from_token(db, authorization)
    settings = get_settings()
    bot = (getattr(settings, "BOT_USERNAME", None) or "").strip()
    if not bot:
        raise HTTPException(status_code=400, detail="BOT_USERNAME not set on server")
    link = f"https://t.me/{bot}?start=ref_{user.tg_user_id}"
    return {"link": link}

@router.get("/progress/referrals/stats")
def referrals_stats(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    user = get_user_from_token(db, authorization)
    invited = db.query(Referral).filter_by(invited_user_id=user.id).first()
    invited_by = invited.inviter_tg_user_id if invited else None
    your_invites = db.query(Referral).filter_by(inviter_tg_user_id=user.tg_user_id).all()
    count = len(your_invites)
    return {
        "you": {"id": user.id, "tg_user_id": user.tg_user_id, "name": user.name, "gems": user.gems},
        "invited_by_tg_user_id": invited_by,
        "your_invited_count": count,
    }