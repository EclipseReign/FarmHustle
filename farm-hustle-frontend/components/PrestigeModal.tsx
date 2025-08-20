"use client";
import { useState } from "react";
import { useGame } from "@/lib/store";

export default function PrestigeModal() {
  const [open, setOpen] = useState(false);
  const prestige = useGame(s => s.prestige);
  const tokens = useGame(s => s.player.prestigeTokens);

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
            <button className="btn" onClick={() => { prestige(); setOpen(false); }}>Confirm</button>
            <button className="btn" onClick={() => setOpen(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}
