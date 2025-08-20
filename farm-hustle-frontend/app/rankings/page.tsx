import Header from "@/components/Header";
import Leaderboard from "@/components/Leaderboard";

export default function Page() {
  return (
    <main>
      <Header />
      <section className="p-4 space-y-4">
        <Leaderboard />
        <div className="card small">
          Prize Pool is tiny & capped; published monthly. Final scores are server authoritative with anti-fraud & KYC threshold.
        </div>
      </section>
    </main>
  );
}
