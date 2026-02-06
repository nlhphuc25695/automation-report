export function StatCard({ title, value, hint }: { title: string; value: string; hint?: string }) {
  return (
    <div className="rounded-2xl border border-ink/10 bg-white/90 p-6 shadow-sm">
      <div className="text-xs uppercase tracking-[0.3em] text-ink/40">{title}</div>
      <div className="mt-3 text-3xl font-display text-ink">{value}</div>
      {hint ? <div className="mt-2 text-sm text-ink/60">{hint}</div> : null}
    </div>
  );
}
