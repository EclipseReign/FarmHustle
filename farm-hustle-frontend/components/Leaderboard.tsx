"use client";
import { useGame } from "@/lib/store";

export default function Leaderboard() {
  const lb = useGame(s => s.leaderboard);
  return (
    <div className="card">
      <div className="font-semibold mb-2">Season Leaderboard (Proxy)</div>
      <ol className="space-y-1">
        {lb.map((e, i) => (
          <li key={e.playerId} className="flex justify-between">
            <span>#{i+1} {e.name}</span>
            <span className="small">{e.skillScore} pts</span>
          </li>
        ))}
      </ol>
      <div className="small mt-2">Final score is server-side & anti-fraud-protected.</div>
    </div>
  );
}
