# Farm Hustle — Frontend (Telegram WebApp)

Next.js (App Router) + Tailwind + Zustand. Designed for Vercel deploy and Telegram Mini App embedding.

## Quick Start
```bash
npm i
npm run dev
```

Open http://localhost:3000

## Deploy (Vercel)
1. Push repo to GitHub.
2. Import to Vercel → Framework: Next.js.
3. Build & deploy. Set your domain as the Mini App URL in BotFather.

## Telegram Mini App Setup
- In `BotFather` set:
  - **Web App URL**: your Vercel URL (e.g., https://farm-hustle.vercel.app)
  - Enable `web_app` menu button or start via deep-link.
- This app auto-reads Telegram theme params and calls `tg.ready()`.

## Environment
Create `.env.local` if you need public vars:
```
NEXT_PUBLIC_BOT_USERNAME=your_bot_name
NEXT_PUBLIC_SEASON_END=2025-09-20
```

## Structure
- `/app` — pages
- `/components` — UI
- `/lib` — telegram integration, economy math, Zustand store
- `/data` — strings
- `/public` — assets

## Game Notes
- This is a **client-first** front that uses local calculations (income, boosts) and a proxy skill score.
- Final authoritative logic (revenue, leaderboard, prize pool, anti-fraud) must live on the backend (next step).
- Prestige/Events pages include the UX flow; API hooks to be wired in backend delivery.

## TODO (when backend arrives)
- Verify Telegram `initData` on server and hydrate profile.
- Sync state to server; reconcile on conflict.
- Event schedule via SSE/polling.
- Leaderboard pagination + your rank.
- Payments: Telegram Stars / other regionals.
