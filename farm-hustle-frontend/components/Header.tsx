"use client";
import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { useGame } from "@/lib/store";
import { initTelegramTheme } from "@/lib/telegram";
import { authWithTelegram } from "@/lib/auth";
import { api } from "@/lib/api";
import { hydrateFromSnapshot } from "@/lib/hydrate";

export default function Header() {
  const cps = useGame(s => s.coinsPerSec);
  const coins = useGame(s => s.player.coins);
  const gems = useGame(s => s.player.gems ?? 0);
  const [authErr, setAuthErr] = useState<string | null>(null);

  useEffect(() => {
    initTelegramTheme();
    (async () => {
      try {
        await authWithTelegram();
        const snap = await api("/me");
        hydrateFromSnapshot(snap);
        setAuthErr(null);
      } catch (e: any) {
        console.warn("Auth/bootstrap failed:", e?.message || e);
        setAuthErr(e?.message || "Auth failed");
      }
    })();

    const id = setInterval(() => useGame.getState().tick(), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className="flex items-center justify-between p-4 sticky top-0 z-30 bg-bg/80 backdrop-blur">
      <div className="flex items-center gap-3">
        <Image src="/logo.svg" alt="logo" width={32} height={32} />
        <div>
          <div className="font-semibold">Farm Hustle</div>
          <div className="small">Coins: {coins.toFixed(0)} • {cps.toFixed(1)}/s</div>
          <div className="small">Gems: {gems}</div>
          {authErr && (
            <div className="small text-red-400">Offline: open from Telegram to sync.</div>
          )}
        </div>
      </div>
      <nav className="flex items-center gap-3">
        <Link className="btn" href="/">Farm</Link>
        <Link className="btn" href="/rankings">Rankings</Link>
        <Link className="btn" href="/events">Events</Link>
        <Link className="btn" href="/prestige">Prestige</Link>
      </nav>
    </header>
  );
}