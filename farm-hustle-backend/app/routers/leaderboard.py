from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from ..db import get_db
from ..models import Leaderboard, User
from ..schemas import LeaderboardOut, LeaderboardItem

router = APIRouter()


def get_uid(authorization: str | None) -> int | None:
    from ..security import decode_jwt

    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    payload = decode_jwt(token)
    return payload.get("uid")


@router.get("", response_model=LeaderboardOut)
def top(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
    limit: int = 50,
):
    uid = get_uid(authorization)
    q = (
        db.query(Leaderboard, User)
        .join(User, Leaderboard.user_id == User.id)
        .order_by(Leaderboard.skill_score.desc())
        .limit(limit)
    )
    top = [
        LeaderboardItem(name=u.name, skill_score=lb.skill_score) for lb, u in q.all()
    ]
    you = None
    your_rank = None
    if uid:
        subq = db.query(Leaderboard).order_by(Leaderboard.skill_score.desc()).all()
        for i, row in enumerate(subq, start=1):
            if row.user_id == uid:
                your_rank = i
                you_user = db.query(User).get(uid)
                you = LeaderboardItem(name=you_user.name, skill_score=row.skill_score)
                break
    return {"top": top, "you": you, "your_rank": your_rank}
