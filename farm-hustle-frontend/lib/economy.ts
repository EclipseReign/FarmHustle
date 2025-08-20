import { Building, Boost, SetBonus } from "./types";

export function incomePerSec(buildings: Building[], boosts: Boost[], sets: SetBonus[], seasonMult: number) {
  const boostMap = new Map<string, number>();
  boosts.forEach(b => b.targetBuildingIds.forEach(id => {
    boostMap.set(id, Math.max(boostMap.get(id) ?? 1, b.multiplier));
  }));
  const setMult = sets.filter(s => s.active).reduce((m, s) => m * s.multiplier, 1);

  return buildings.reduce((sum, b) => {
    const base = b.baseIncomePerSec * Math.max(1, b.level);
    const boost = boostMap.get(b.id) ?? 1;
    return sum + base * boost;
  }, 0) * setMult * seasonMult;
}

export function upgradeCost(b: Building) {
  return Math.floor(b.upgradeCost * Math.pow(1.15, b.level));
}

export function skillScoreProxy(income: number, setsActive: number, boostsUsed: number) {
  const a = Math.log10(1 + income) * 40;
  const b = Math.min(setsActive, 5) * 25;
  const c = Math.min(boostsUsed, 20) * 1.5;
  return Math.round(a + b + c);
}
