export default function EventBanner({ title, text }: { title: string; text: string }) {
  return (
    <div className="card border-accent/40">
      <div className="font-semibold">{title}</div>
      <div className="small">{text}</div>
    </div>
  );
}
