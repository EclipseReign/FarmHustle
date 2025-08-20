# Farm Hustle — Backend (FastAPI + PostgreSQL)

Production-ready skeleton for Railway. Provides:
- Telegram WebApp auth (initData verification)
- User/profile bootstrap
- Authoritative actions: rotate boosts, upgrade building, prestige
- Season/leaderboard with capped tiny prize pool
- Basic anti-fraud (rate checks), server-side Skill Score proxy
- Admin endpoints to set monthly net revenue and finalize payouts

## Quick Start (local)
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost:5432/farmhustle
export BOT_TOKEN=123456:ABC-DEF
export JWT_SECRET=change_me
uvicorn app.main:app --reload
Open http://localhost:8000/docs

Railway
Add a PostgreSQL plugin (copy connection URL to DATABASE_URL).

Set variables: DATABASE_URL, BOT_TOKEN, JWT_SECRET, ALLOWED_ORIGINS (comma-separated).

Start command: uvicorn app.main:app --host 0.0.0.0 --port ${PORT}

First boot auto-creates tables (SQLAlchemy).

Endpoints (high-level)
POST /auth/telegram — verify initData, upsert user, returns JWT.

GET /me — profile + snapshot.

POST /game/rotate — rotate Hot Zones (server chooses targets).

POST /game/upgrade — upgrade a building (server checks coins/cost).

POST /game/prestige — prestige (reset + token).

GET /leaderboard — top N + your rank.

GET /season — current season info + prize pool computed (min/cap).

POST /admin/season/net — set net revenue for the month.

POST /admin/season/finalize — compute & store prize distribution.

Security
JWT in Authorization: Bearer <token> from /auth/telegram.

Telegram initData verification via HMAC-SHA256 (see security.py).

Basic action rate checks + anomalous CPS flags (extend in production).

Notes
All economy is server-side in economy.py (mirror with frontend for UX; server is authoritative).

Replace stubbed token math with your exact balance design when ready.
