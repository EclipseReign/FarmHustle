
export const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL || "";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("fh_token");
}
export function setToken(t: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("fh_token", t);
}

export async function api<T = any>(path: string, opts: RequestInit = {}): Promise<T> {
  if (!API_BASE) {
    throw new Error("NEXT_PUBLIC_BACKEND_URL is not set");
  }
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts.headers as Record<string,string> || {}),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers, cache: "no-store" });
  if (!res.ok) {
    const text = await res.text().catch(()=> "");
    throw new Error(`${res.status} ${res.statusText} ${text}`);
  }
  return res.json();
}
