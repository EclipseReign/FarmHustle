'use client';
import Header from "@/components/Header";
import BuildingCard from "@/components/BuildingCard";
import BoostTimer from "@/components/BoostTimer";
import SetBonusCard from "@/components/SetBonusCard";
import EventBanner from "@/components/EventBanner";
import { useGame } from "@/lib/store";

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
  const rotate = useGame(s => s.triggerBoostRotation);
  return <button className="btn" onClick={rotate}>Rotate Hot Zones</button>;
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
