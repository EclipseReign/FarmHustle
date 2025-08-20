
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, UserBuilding
from ..schemas import AuthIn, TokenOut, SnapshotOut, BuildingOut, BoostOut
from ..security import verify_telegram_init_data, make_jwt, decode_jwt
from ..economy import ensure_user_buildings, CATALOG, current_income_per_sec
from datetime import datetime

router = APIRouter(tags=["auth"])

def get_user_from_token(db: Session, auth_header: str | None) -> User:
if not auth_header or not auth_header.lower().startswith("bearer "):
raise HTTPException(status_code=401, detail="Missing token")
token = auth_header.split(" ",1)[1]
payload = decode_jwt(token)
uid = payload.get("uid")
if not uid:
raise HTTPException(status_code=401, detail="Invalid token payload")
user = db.get(User, uid)
if not user:
raise HTTPException(status_code=401, detail="Unknown user")
return user

@router.post("/auth/telegram", response_model=TokenOut)
def auth_telegram(body: AuthIn, db: Session = Depends(get_db)):
data = verify_telegram_init_data(body.init_data)
tg_user = data.get("user")
# If user is URL-encoded JSON, parse; else it's string
import json
if isinstance(tg_user, str):
try:
tg_user = json.loads(tg_user)
except Exception:
pass
tg_id = str(tg_user.get("id"))
name = tg_user.get("username") or tg_user.get("first_name") or "Player"
user = db.query(User).filter_by(tg_user_id=tg_id).first()
if not user:
user = User(tg_user_id=tg_id, name=name)
db.add(user)
db.flush()
# give starter buildings
from ..economy import ensure_user_buildings
ensure_user_buildings(db, user)
else:
user.name = name
# refresh cps
user.cps_cached = current_income_per_sec(user)
user.last_tick_at = datetime.utcnow()
db.commit()
token = make_jwt({"uid": user.id, "tg": tg_id})
return {"token": token}

@router.get("/me", response_model=SnapshotOut)
def me(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
user = get_user_from_token(db, authorization)
from ..economy import current_income_per_sec
cps = current_income_per_sec(user)
user.cps_cached = cps
db.commit()

python
Всегда показывать подробности

Копировать
buildings = []
for ub in user.buildings:
    c = CATALOG[ub.building_id]
    buildings.append(BuildingOut(
        id=ub.building_id, name=c["name"], level=ub.level,
        baseIncomePerSec=c["baseIncomePerSec"], upgradeCost=c["upgradeCost"]
    ))
boosts = []
for b in user.boosts:
    if b.ends_at > datetime.utcnow():
        boosts.append(BoostOut(id=b.id, label=b.label, multiplier=b.multiplier, ends_at=b.ends_at, target_ids=b.targets.get("ids", [])))
return {
    "name": user.name,
    "coins": user.coins,
    "gems": user.gems,
    "prestige_tokens": user.prestige_tokens,
    "season_multiplier_paid": user.season_multiplier_paid,
    "coins_per_sec": cps,
    "boosts_used": user.boosts_used,
    "buildings": buildings,
    "boosts": boosts
}
