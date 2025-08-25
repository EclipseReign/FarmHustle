# app/models.py
from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, JSON, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tg_user_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    coins: Mapped[float] = mapped_column(Float, default=200)
    gems: Mapped[int] = mapped_column(Integer, default=0)
    prestige_tokens: Mapped[int] = mapped_column(Integer, default=0)
    season_multiplier_paid: Mapped[float] = mapped_column(Float, default=1.0)
    boosts_used: Mapped[int] = mapped_column(Integer, default=0)
    cps_cached: Mapped[float] = mapped_column(Float, default=0.0)
    last_tick_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    buildings: Mapped[List["UserBuilding"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    boosts: Mapped[List["UserBoost"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class UserBuilding(Base):
    __tablename__ = "user_buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    building_id: Mapped[str] = mapped_column(String(32), index=True)  # 'grain', 'dairy', ...
    level: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="buildings")

class UserBoost(Base):
    __tablename__ = "user_boosts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    label: Mapped[str] = mapped_column(String(64))
    multiplier: Mapped[float] = mapped_column(Float, default=3.0)
    ends_at: Mapped[datetime] = mapped_column(DateTime)
    targets: Mapped[dict] = mapped_column(JSON)  # {"ids": ["grain","dairy"]}

    user: Mapped["User"] = relationship(back_populates="boosts")

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    skill_score: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime)
    ends_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(16), default="active")  # active|ended
    net_revenue_usd: Mapped[float] = mapped_column(Float, default=0.0)
    prize_pool_final_usd: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PrizePayout(Base):
    __tablename__ = "prize_payouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    rank: Mapped[int] = mapped_column(Integer)
    amount_usd: Mapped[float] = mapped_column(Float)
    

class DailyClaim(Base):
    __tablename__ = "daily_claims"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    claimed_on: Mapped[datetime] = mapped_column(Date)  # store date only
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "claimed_on", name="uq_daily_per_user_day"),)

class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(primary_key=True)
    inviter_tg_user_id: Mapped[str] = mapped_column(String(32), index=True)
    invited_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
