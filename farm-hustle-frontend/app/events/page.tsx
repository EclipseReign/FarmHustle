'use client';
import Header from "@/components/Header";
import EventBanner from "@/components/EventBanner";
import { api } from "@/lib/api";
import { useState } from "react";
import { useGame } from "@/lib/store";

export default function Page() {
  const [dailyMsg, setDailyMsg] = useState<string | null>(null);
  const [inviteLink, setInviteLink] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const gems = useGame(s => s.player.gems ?? 0);
  const [refStats, setRefStats] = useState<any>(null);

  async function claimDaily() {
    setError(null); setDailyMsg(null);
    try {
      const res = await api<{ok:boolean; coins_added:number; claimed_on:string}>('/progress/daily/claim', { method: 'POST' });
      setDailyMsg(`+${res.coins_added} coins (${new Date(res.claimed_on).toDateString()})`);
    } catch (e:any) {
      setError(e?.message || 'Claim failed');
    }
  }

  async function getInvite() {
    setError(null);
    try {
      const res = await api<{startapp_link:string; fallback_start_link:string}>("/progress/invite_link");
      const link = res.startapp_link || res.fallback_start_link;
      setInviteLink(link);
      try { await navigator.clipboard.writeText(link); } catch {}
    } catch (e:any) {
      setError(e?.message || "Invite link error");
    }
  }

  async function loadRefStats() {
    setError(null);
    try {
      const res = await api('/progress/referrals/stats');
      setRefStats(res);
    } catch (e:any) {
      setError(e?.message || 'Stats error');
    }
  }

  return (
    <main>
      <Header />
      <section className="p-4 space-y-4">
        <div className="card">
          <div className="font-semibold mb-1">Your Gems: {gems}</div>
          <div className="small opacity-80">Get +5 gems for each invited friend (they get +2).</div>
        </div>

        <EventBanner title="Daily Bonus" text="Claim once per day to keep the growth going." />
        <button className="btn" onClick={claimDaily}>Claim Daily</button>
        {dailyMsg && <div className="small text-green-300">{dailyMsg}</div>}

        <EventBanner title="Invite Friends" text="Share the game. When they join, you both get a tiny bonus." />
        <button className="btn" onClick={getInvite}>Get Invite Link</button>
        {inviteLink && <div className="small break-all">
          <div>StartApp Link (recommended):</div>
          <div>{inviteLink}</div>
        </div>}

        <div className="card">
          <div className="font-semibold mb-2">Referral Stats</div>
          <div className="small mb-2">Check that invites are counted correctly.</div>
          <button className="btn" onClick={loadRefStats}>Load Stats</button>
          {refStats && (
            <pre className="small mt-2 whitespace-pre-wrap break-all">{JSON.stringify(refStats, null, 2)}</pre>
          )}
        </div>

        {error && <div className="small text-red-400">{error}</div>}
      </section>
    </main>
  );
}