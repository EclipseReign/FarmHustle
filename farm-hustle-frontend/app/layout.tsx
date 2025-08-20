import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Farm Hustle",
  description: "Telegram Tycoon-Clicker — Season-based farm hustle",
  manifest: "/site.webmanifest",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
