declare global {
  interface Window {
    Telegram?: any;
  }
}

export function initTelegramTheme() {
  if (typeof window === "undefined") return;
  const tg = window.Telegram?.WebApp;
  try {
    tg?.expand();
    tg?.ready();
  } catch {}
  const params = tg?.themeParams || {};
  const root = document.documentElement;
  if (params && Object.keys(params).length) {
    const bg = params.bg_color || "#0c0f14";
    const fg = params.text_color || "#f4f6f8";
    const accent = params.button_color || "#84cc16";
    const card = params.secondary_bg_color || "#151a22";
    root.style.setProperty("--bg", bg);
    root.style.setProperty("--fg", fg);
    root.style.setProperty("--accent", accent);
    root.style.setProperty("--card", card);
  }
}
