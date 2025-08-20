from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    Boolean,
    JSON,
    UniqueConstraint,
    Text,
)
from datetime import datetime
from .db import Base


class User(Base):
    tablename = "users"
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    buildings: Mapped[list["UserBuilding"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    boosts: Mapped[list["UserBoost"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserBuilding(Base):
    tablename = "user_buildings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    building_id: Mapped[str] = mapped_column(
        String(32), index=True
    )  # 'grain','dairy', etc.
    level: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped[User] = relationship(back_populates="buildings")
    table_args = (UniqueConstraint("user_id", "building_id", name="uq_user_building"),)


class UserBoost(Base):
    tablename = "user_boosts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    label: Mapped[str] = mapped_column(String(64))
    multiplier: Mapped[float] = mapped_column(Float, default=3.0)
    ends_at: Mapped[datetime] = mapped_column(DateTime)
    targets: Mapped[dict] = mapped_column(JSON)  # { "ids": ["grain","dairy"] }
    user: Mapped[User] = relationship(back_populates="boosts")


class Leaderboard(Base):
    tablename = "leaderboard"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    skill_score: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Season(Base):
    tablename = "seasons"
    id: Mapped[int] = mapped_column(primary_key=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime)
    ends_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(16), default="active")  # active|ended
    net_revenue_usd: Mapped[float] = mapped_column(Float, default=0.0)
    prize_pool_final_usd: Mapped[float] = mapped_column(
        Float, default=0.0
    )  # after finalize
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PrizePayout(Base):
    tablename = "prize_payouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    rank: Mapped[int] = mapped_column(Integer)
    amount_usd: Mapped[float] = mapped_column(Float)
