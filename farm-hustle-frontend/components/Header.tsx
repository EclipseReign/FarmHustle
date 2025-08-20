"use client";
import Link from "next/link";
import Image from "next/image";
import { useEffect } from "react";
import { useGame } from "@/lib/store";
import { initTelegramTheme } from "@/lib/telegram";

export default function Header() {
  const cps = useGame(s => s.coinsPerSec);
  const coins = useGame(s => s.player.coins);
  useEffect(() => {
    initTelegramTheme();
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
