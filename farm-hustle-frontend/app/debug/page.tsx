"use client";
import { useEffect, useState } from "react";

export default function DebugPage() {
  const [info, setInfo] = useState<any>({});
  const [resp, setResp] = useState<any>(null);
  const [err, setErr] = useState<string>("");

  useEffect(() => {
    const tg: any = (globalThis as any).Telegram?.WebApp;
    const initData: string = tg?.initData || "";
    const initSafe: any = tg?.initDataUnsafe || null;

    setInfo({
      platform: tg?.platform,
      version: tg?.version,
      backend: process.env.NEXT_PUBLIC_BACKEND_URL,
      initLen: initData?.length || 0,
      hasHash: typeof initData === "string" && initData.includes("hash="),
      user: initSafe?.user || null,
    });

    if (initData) {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/telegram`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ init_data: initData }),
      })
        .then(async (r) => setResp({ status: r.status, body: await r.text() }))
        .catch((e) => setErr(String(e)));
    }
  }, []);

  const copy = async () => {
    try {
      const tg: any = (globalThis as any).Telegram?.WebApp;
      await navigator.clipboard.writeText(tg?.initData || "");
      alert("initData скопирован");
    } catch (e:any) { alert(e?.message || String(e)); }
  };

  return (
    <div style={{ padding: 16 }}>
      <h1>WebApp Debug</h1>
      <pre>{JSON.stringify(info, null, 2)}</pre>
      <button onClick={copy}>Скопировать initData</button>
      {err && <pre>ERR: {err}</pre>}
      {resp && <pre>AUTH /auth/telegram → {resp.status}\n{resp.body}</pre>}
    </div>
  );
}
