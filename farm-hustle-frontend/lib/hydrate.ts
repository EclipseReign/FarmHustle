
'use client';
import { useGame } from "@/lib/store";

export type ServerSnapshot = {
  name: string;
  coins: number;
  gems: number;
  prestige_tokens: number;
  season_multiplier_paid: number;
  coins_per_sec: number;
  boosts_used: number;
  buildings: { id: string; name: string; level: number; baseIncomePerSec: number; upgradeCost: number }[];
  boosts: { id: number; label: string; multiplier: number; ends_at: string; target_ids: string[] }[];
};

export function hydrateFromSnapshot(snap: ServerSnapshot) {
  const s = useGame.getState();
  const player = {
    ...s.player,
    coins: snap.coins,
    gems: snap.gems,
    prestigeTokens: snap.prestige_tokens,
    seasonMultiplierPaid: snap.season_multiplier_paid,
  };
  const buildings = s.buildings.map((b) => {
    const srv = snap.buildings.find((x) => x.id === b.id);
    return srv ? { ...b, level: srv.level } : b;
  });
  const boosts = snap.boosts.map((b) => ({
    id: String(b.id),
    label: b.label,
    multiplier: b.multiplier,
    secondsLeft: Math.max(0, Math.floor((new Date(b.ends_at).getTime() - Date.now())/1000)),
    targetBuildingIds: b.target_ids,
  }));
  useGame.setState({
    player,
    buildings,
    boosts,
    boostsUsed: snap.boosts_used,
    coinsPerSec: snap.coins_per_sec,
  });
}
