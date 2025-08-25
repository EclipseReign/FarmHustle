
"use client";
import { useState } from "react";
import { useGame } from "@/lib/store";
import { api } from "@/lib/api";
import { hydrateFromSnapshot } from "@/lib/hydrate";

export default function PrestigeModal() {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const tokens = useGame(s => s.player.prestigeTokens);

  const onConfirm = async () => {
    if (busy) return;
    setBusy(true);
    try {
      const snap = await api("/game/prestige", { method: "POST" });
      hydrateFromSnapshot(snap);
      setOpen(false);
    } catch (e: any) {
      console.warn("Prestige failed:", e?.message || e);
      alert("Prestige failed. Please open from Telegram WebApp and try again.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <div className="font-semibold">Prestige</div>
          <div className="small">Tokens: {tokens}</div>
        </div>
        <button className="btn" onClick={() => setOpen(true)}>Prestige Now</button>
      </div>
      {open && (
        <div className="mt-3 p-3 rounded-2xl border border-white/10 bg-white/5">
          <div className="mb-2">Convert progress into permanent tiny bonus and reset early buildings.</div>
          <div className="flex gap-2">
            <button className="btn" onClick={onConfirm}>{busy ? "..." : "Confirm"}</button>
            <button className="btn" onClick={() => setOpen(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}
