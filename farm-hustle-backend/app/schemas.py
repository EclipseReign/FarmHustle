from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AuthIn(BaseModel):
    init_data: str


class TokenOut(BaseModel):
    token: str


class BuildingOut(BaseModel):
    id: str
    name: str
    level: int
    baseIncomePerSec: float
    upgradeCost: int


class BoostOut(BaseModel):
    id: int
    label: str
    multiplier: float
    ends_at: datetime
    target_ids: List[str]


class SnapshotOut(BaseModel):
    name: str
    coins: float
    gems: int
    prestige_tokens: int
    season_multiplier_paid: float
    coins_per_sec: float
    boosts_used: int
    buildings: List[BuildingOut]
    boosts: List[BoostOut]


class UpgradeIn(BaseModel):
    building_id: str


class LeaderboardItem(BaseModel):
    name: str
    skill_score: int


class LeaderboardOut(BaseModel):
    top: List[LeaderboardItem]
    you: Optional[LeaderboardItem] = None
    your_rank: Optional[int] = None


class SeasonOut(BaseModel):
    id: int
    starts_at: datetime
    ends_at: datetime
    status: str
    net_revenue_usd: float
    prize_pool_preview_usd: float
    cap_usd: float
    min_usd: float


class SetNetRevenueIn(BaseModel):
    season_id: int
    net_revenue_usd: float


class FinalizeOut(BaseModel):
    season_id: int
    pool_final_usd: float
    distribution: List[dict]
