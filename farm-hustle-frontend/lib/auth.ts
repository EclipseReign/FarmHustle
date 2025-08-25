
import { api, setToken, getToken } from "./api";

declare global {
  interface Window { Telegram?: any; }
}

export async function authWithTelegram(): Promise<string> {
  if (typeof window === "undefined") throw new Error("client only");
  const tg = window.Telegram?.WebApp;
  const initData = tg?.initData;
  const existing = getToken();
  if (existing) return existing;

  if (!initData) {
    throw new Error("No initData — open from Telegram WebApp");
  }
  const { token } = await api<{token:string}>("/auth/telegram", {
    method: "POST",
    body: JSON.stringify({ init_data: initData }),
  });
  setToken(token);
  return token;
}
