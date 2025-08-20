"use client";

import { create } from "zustand";
import { Building, Boost, SetBonus, Player, LeaderboardEntry, EventDef } from "./types";
import { incomePerSec, skillScoreProxy } from "./economy";

type State = {
  player: Player;
  buildings: Building[];
  boosts: Boost[];
  sets: SetBonus[];
  events: EventDef[];
  coinsPerSec: number;
  boostsUsed: number;
  leaderboard: LeaderboardEntry[];
  tick: () => void;
  upgrade: (id: string) => void;
  triggerBoostRotation: () => void;
  spendGems: (g: number) => boolean;
  prestige: () => void;
  addEvent: (ev: EventDef) => void;
  endEvent: (id: string) => void;
  recompute: () => void;
};

const starterBuildings: Building[] = [
  { id: "grain", name: "Grain Field", level: 1, baseIncomePerSec: 1, upgradeCost: 20, setKey: "dairy" },
  { id: "dairy", name: "Dairy Shed", level: 0, baseIncomePerSec: 4, upgradeCost: 60, setKey: "dairy" },
  { id: "grove", name: "Fruit Grove", level: 0, baseIncomePerSec: 3, upgradeCost: 50, setKey: "grove" },
  { id: "apiary", name: "Apiary", level: 0, baseIncomePerSec: 5, upgradeCost: 80, setKey: "grove" }
];

const starterSets: SetBonus[] = [
  { key: "dairy", label: "Cheesemaker’s Guild", description: "+10% income when Grain+Dairy 3/2", requiredIds: ["grain","dairy"], active: true, multiplier: 1.10 },
  { key: "grove", label: "Sunrise Orchard", description: "+8% income when Grove+Apiary 2/1", requiredIds: ["grove","apiary"], active: false, multiplier: 1.08 },
];

const starterBoosts: Boost[] = [
  { id: "b1", label: "Hot Zone", multiplier: 3, secondsLeft: 600, targetBuildingIds: ["grain"] }
];

const starterEvents: EventDef[] = [];

const starterPlayer: Player = {
  id: "me", name: "You", coins: 200, gems: 0, prestigeTokens: 0, seasonMultiplierPaid: 1.0
};

export const useGame = create<State>((set, get) => ({
  player: starterPlayer,
  buildings: starterBuildings,
  boosts: starterBoosts,
  sets: starterSets,
  events: starterEvents,
  coinsPerSec: 0,
  boostsUsed: 0,
  leaderboard: [
    { playerId: "max", name: "Max", skillScore: 1200 },
    { playerId: "ava", name: "Ava", skillScore: 950 },
    { playerId: "you", name: "You", skillScore: 400 },
  ],
  recompute: () => {
    const s = get();
    const cps = incomePerSec(s.buildings, s.boosts, s.sets, s.player.seasonMultiplierPaid || 1);
    set({ coinsPerSec: cps });
  },
  tick: () => {
    const s = get();
    const cps = s.coinsPerSec || incomePerSec(s.buildings, s.boosts, s.sets, s.player.seasonMultiplierPaid || 1);
    const player = { ...s.player, coins: s.player.coins + cps };
    const boosts = s.boosts.map(b => ({...b, secondsLeft: Math.max(0, b.secondsLeft - 1)})).filter(b => b.secondsLeft > 0);
    set({ player, boosts, coinsPerSec: cps });
    const setsActive = s.sets.filter(x => x.active).length;
    const youScore = skillScoreProxy(cps, setsActive, s.boostsUsed);
    const leaderboard = [
      { playerId: "max", name: "Max", skillScore: 1200 },
      { playerId: "ava", name: "Ava", skillScore: 950 },
      { playerId: "you", name: "You", skillScore: youScore },
    ].sort((a,b)=> b.skillScore - a.skillScore);
    set({ leaderboard });
  },
  upgrade: (id: string) => {
    const s = get();
    const idx = s.buildings.findIndex(b => b.id === id);
    if (idx < 0) return;
    const b = s.buildings[idx];
    const cost = Math.floor(20 * Math.pow(1.15, b.level) + b.upgradeCost);
    if (s.player.coins < cost) return;
    const buildings = [...s.buildings];
    buildings[idx] = { ...b, level: b.level + 1 };
    const player = { ...s.player, coins: s.player.coins - cost };
    set({ buildings, player });
    get().recompute();
  },
  triggerBoostRotation: () => {
    const s = get();
    const ids = s.buildings.map(b => b.id);
    const shuffled = [...ids].sort(()=> Math.random()-0.5).slice(0,2);
    const boost: Boost = {
      id: `rot-${Date.now()}`, label: "Hot Zone", multiplier: 3, secondsLeft: 600, targetBuildingIds: shuffled
    };
    set({ boosts: [boost, ...s.boosts], boostsUsed: s.boostsUsed + 1 });
    get().recompute();
  },
  spendGems: (g: number) => {
    const s = get();
    if (s.player.gems < g) return false;
    set({ player: { ...s.player, gems: s.player.gems - g } });
    return true;
  },
  prestige: () => {
    const s = get();
    const newToken = Math.random() < 0.9 ? 1 : 0; // stub; backend authoritative
    const player = {
      ...s.player,
      prestigeTokens: s.player.prestigeTokens + newToken,
      coins: 200
    };
    const buildings = s.buildings.map(b => ({...b, level: b.id === "grain" ? 1 : 0 }));
    set({ player, buildings });
    get().recompute();
  },
  addEvent: (ev: EventDef) => {
    const s = get();
    set({ events: [ev, ...s.events] });
  },
  endEvent: (id: string) => {
    const s = get();
    set({ events: s.events.filter(e => e.id !== id) });
  },
}));
