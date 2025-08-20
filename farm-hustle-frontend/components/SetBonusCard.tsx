import { SetBonus } from "@/lib/types";

export default function SetBonusCard({ s }: { s: SetBonus }) {
  return (
    <div className="card">
      <div className="font-semibold">{s.label} {s.active ? "✅" : "⏳"}</div>
      <div className="small">{s.description} • x{(s.multiplier).toFixed(2)}</div>
    </div>
  );
}
