
from math import log10, floor
from typing import List, Dict
from datetime import datetime, timedelta
from .models import User, UserBuilding, UserBoost
from sqlalchemy.orm import Session

CATALOG = {
"grain": {"name":"Grain Field","baseIncomePerSec":1.0,"upgradeCost":20},
"dairy": {"name":"Dairy Shed","baseIncomePerSec":4.0,"upgradeCost":60},
"grove": {"name":"Fruit Grove","baseIncomePerSec":3.0,"upgradeCost":50},
"apiary": {"name":"Apiary","baseIncomePerSec":5.0,"upgradeCost":80},
}

SET_BONUSES = [
{"key":"dairy","label":"Cheesemaker’s Guild","required":["grain","dairy"],"multiplier":1.10},
{"key":"grove","label":"Sunrise Orchard","required":["grove","apiary"],"multiplier":1.08},
]

def ensure_user_buildings(db: Session, user: User):
have = {b.building_id for b in user.buildings}
for bid in CATALOG.keys():
if bid not in have:
db.add(UserBuilding(user_id=user.id, building_id=bid, level=1 if bid=="grain" else 0))
db.flush()

def active_set_multiplier(buildings: List[UserBuilding]) -> float:
ids = {b.building_id for b in buildings if b.level>0}
mult = 1.0
for s in SET_BONUSES:
if all(x in ids for x in s["required"]):
mult *= s["multiplier"]
return mult

def current_income_per_sec(user: User) -> float:
# compute boost map
now = datetime.utcnow()
boost_map: Dict[str, float] = {}
for b in user.boosts:
if b.ends_at > now:
for bid in b.targets.get("ids", []):
boost_map[bid] = max(boost_map.get(bid, 1.0), b.multiplier)
base = 0.0
for ub in user.buildings:
c = CATALOG[ub.building_id]
base_cps = c["baseIncomePerSec"] * max(1, ub.level)
mult = boost_map.get(ub.building_id, 1.0)
base += base_cps * mult
return base * active_set_multiplier(user.buildings) * max(1.0, user.season_multiplier_paid)

def upgrade_cost(bid: str, level: int) -> int:
c = CATALOG[bid]
return floor(20 * (1.15 ** level) + c["upgradeCost"])

def skill_score_proxy(cps: float, sets_active: int, boosts_used: int) -> int:
a = log10(1 + cps) * 40
b = min(sets_active, 5) * 25
c = min(boosts_used, 20) * 1.5
return round(a + b + c)

def sets_active(buildings: List[UserBuilding]) -> int:
ids = {b.building_id for b in buildings if b.level>0}
count = 0
for s in SET_BONUSES:
if all(x in ids for x in s["required"]):
count += 1
return count
