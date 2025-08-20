import Header from "@/components/Header";
import PrestigeModal from "@/components/PrestigeModal";

export default function Page() {
  return (
    <main>
      <Header />
      <section className="p-4 space-y-4">
        <PrestigeModal />
        <div className="card small">
          Prestige resets early buildings for permanent season power. Server will compute exact token yield.
        </div>
      </section>
    </main>
  );
}
