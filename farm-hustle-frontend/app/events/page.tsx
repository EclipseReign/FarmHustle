import Header from "@/components/Header";
import EventBanner from "@/components/EventBanner";

export default function Page() {
  return (
    <main>
      <Header />
      <section className="p-4 space-y-4">
        <EventBanner title="County Fair" text="Timed sell multiplier event. Coming soon." />
        <EventBanner title="Storm Alert" text="Prepare buildings or use Midnight Overdrive to avoid penalties." />
        <EventBanner title="Market Raid" text="Fast sell cycle and sub-challenges." />
      </section>
    </main>
  );
}
