"use client";
import { Building } from "@/lib/types";
import { useGame } from "@/lib/store";

export default function BuildingCard({ b }: { b: Building }) {
  const upgrade = useGame(s => s.upgrade);
  const cps = (b.baseIncomePerSec * Math.max(1, b.level)).toFixed(1);
  const cost = Math.floor(20 * Math.pow(1.15, b.level) + b.upgradeCost);
  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <div className="font-semibold">{b.name} <span className="small">Lv {b.level}</span></div>
          <div className="small">Income: {cps}/s</div>
        </div>
        <button onClick={() => upgrade(b.id)} className="btn">Upgrade • {cost}</button>
      </div>
    </div>
  );
}
