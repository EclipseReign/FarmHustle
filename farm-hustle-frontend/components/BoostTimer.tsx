"use client";
import { Boost } from "@/lib/types";

export default function BoostTimer({ b }: { b: Boost }) {
  const m = Math.floor(b.secondsLeft/60);
  const s = b.secondsLeft%60;
  return (
    <div className="card">
      <div className="font-semibold">{b.label} ×{b.multiplier.toFixed(1)}</div>
      <div className="small">Targets: {b.targetBuildingIds.join(", ")} • {m}:{s.toString().padStart(2,"0")}</div>
    </div>
  );
}
