
"use client";
import { Building } from "@/lib/types";
import { api } from "@/lib/api";
import { hydrateFromSnapshot } from "@/lib/hydrate";
import { useState } from "react";

export default function BuildingCard({ b }: { b: Building }) {
  const [busy, setBusy] = useState(false);
  const cps = (b.baseIncomePerSec * Math.max(1, b.level)).toFixed(1);
  const cost = Math.floor(20 * Math.pow(1.15, b.level) + b.upgradeCost);

  const onUpgrade = async () => {
    if (busy) return;
    setBusy(true);
    try {
      const snap = await api("/game/upgrade", {
        method: "POST",
        body: JSON.stringify({ building_id: b.id }),
      });
      hydrateFromSnapshot(snap);
    } catch (e: any) {
      console.warn("Upgrade failed:", e?.message || e);
      alert("Upgrade failed. Make sure you have enough coins and are authenticated via Telegram.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <div className="font-semibold">{b.name} <span className="small">Lv {b.level}</span></div>
          <div className="small">Income: {cps}/s</div>
        </div>
        <button onClick={onUpgrade} className="btn" disabled={busy}>
          {busy ? "..." : `Upgrade • ${cost}`}
        </button>
      </div>
    </div>
  );
}
