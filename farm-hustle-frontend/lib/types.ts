export type BuildingId = string;

export interface Building {
  id: BuildingId;
  name: string;
  level: number;
  baseIncomePerSec: number;
  upgradeCost: number;
  setKey?: string;
}

export interface Boost {
  id: string;
  label: string;
  multiplier: number;
  secondsLeft: number;
  targetBuildingIds: BuildingId[];
}

export interface SetBonus {
  key: string;
  label: string;
  description: string;
  requiredIds: BuildingId[];
  active: boolean;
  multiplier: number;
}

export interface Player {
  id: string;
  name: string;
  coins: number;
  gems: number;
  prestigeTokens: number;
  seasonMultiplierPaid: number;
}

export interface LeaderboardEntry {
  playerId: string;
  name: string;
  skillScore: number;
}

export interface EventDef {
  id: string;
  title: string;
  description: string;
  durationSec: number;
  effect: "sell_bonus" | "storm_penalty" | "night_overdrive" | "locust_minigame";
  value: number;
}
