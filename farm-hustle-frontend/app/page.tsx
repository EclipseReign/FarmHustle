
'use client';
import Header from "@/components/Header";
import BuildingCard from "@/components/BuildingCard";
import BoostTimer from "@/components/BoostTimer";
import SetBonusCard from "@/components/SetBonusCard";
import EventBanner from "@/components/EventBanner";
import { useGame } from "@/lib/store";
import { api } from "@/lib/api";
import { hydrateFromSnapshot } from "@/lib/hydrate";

export default function Page() {
  return (
    <main>
      <Header />
      <section className="p-4 space-y-4">
        <EventBanner title="Hot Zones" text="Tap Rotate to reroll which buildings are boosted x3 for 10 minutes." />
        <RotateButton />
        <FarmGrid />
        <SetsGrid />
        <BoostsGrid />
        <div className="small">Tip: Time upgrades when targets are in Hot Zone.</div>
      </section>
    </main>
  );
}

function RotateButton() {
  const rotateLocal = useGame(s => s.triggerBoostRotation);
  const onClick = async () => {
    try {
      await api("/game/rotate", { method: "POST" });
      const snap = await api("/me");
      hydrateFromSnapshot(snap);
    } catch (e) {
      console.warn("Server rotate failed, using local fallback.", e);
      rotateLocal();
    }
  };
  return <button className="btn" onClick={onClick}>Rotate Hot Zones</button>;
}

function FarmGrid() {
  const buildings = useGame(s => s.buildings);
  return (
    <div className="grid-cards">
      {buildings.map(b => <BuildingCard key={b.id} b={b} />)}
    </div>
  );
}

function SetsGrid() {
  const sets = useGame(s => s.sets);
  return (
    <div className="grid-cards">
      {sets.map(s => <SetBonusCard key={s.key} s={s} />)}
    </div>
  );
}

function BoostsGrid() {
  const boosts = useGame(s => s.boosts);
  if (!boosts.length) return null;
  return (
    <div className="grid-cards">
      {boosts.map(b => <BoostTimer key={b.id} b={b} />)}
    </div>
  );
}
