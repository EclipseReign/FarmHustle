'use client';
import Header from "@/components/Header";
import EventBanner from "@/components/EventBanner";
import { api } from "@/lib/api";
import { useState } from "react";

export default function Page() {
  const [dailyMsg, setDailyMsg] = useState<string | null>(null);
  const [inviteLink, setInviteLink] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

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
      const res = await api<{link:string}>('/progress/invite_link');
      setInviteLink(res.link);
      try {
        await navigator.clipboard.writeText(res.link);
      } catch {}
    } catch (e:any) {
      setError(e?.message || 'Invite link error');
    }
  }

  return (
    <main>
      <Header />
      <section className="p-4 space-y-4">
        <EventBanner title="Daily Bonus" text="Claim once per day to keep the growth going." />
        <button className="btn" onClick={claimDaily}>Claim Daily</button>
        {dailyMsg && <div className="small text-green-300">{dailyMsg}</div>}

        <EventBanner title="Invite Friends" text="Share the game. When they join, you both get a tiny bonus." />
        <button className="btn" onClick={getInvite}>Get Invite Link</button>
        {inviteLink && <div className="small break-all">{inviteLink}</div>}

        {error && <div className="small text-red-400">{error}</div>}
      </section>
    </main>
  );
}