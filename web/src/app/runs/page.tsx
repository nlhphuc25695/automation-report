import { AppShell } from "@/components/AppShell";

const runs = [
  { client: "Client A", month: "2026-01", status: "Success", rows: "12,540" },
  { client: "Client B", month: "2026-01", status: "Partial", rows: "8,210" },
  { client: "Client C", month: "2026-01", status: "Failed", rows: "0" },
];

export default function RunsPage() {
  return (
    <AppShell>
      <div>
        <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Runs & Logs</div>
        <h1 className="mt-2 font-display text-4xl text-ink">Execution History</h1>
      </div>

      <div className="mt-8 space-y-4">
        {runs.map((run) => (
          <div key={`${run.client}-${run.month}`} className="rounded-2xl border border-ink/10 bg-white/90 p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-lg font-semibold text-ink">{run.client}</div>
                <div className="text-sm text-ink/60">Month: {run.month}</div>
              </div>
              <div className="rounded-full bg-ink/10 px-3 py-1 text-xs font-semibold text-ink">
                {run.status}
              </div>
            </div>
            <div className="mt-3 text-sm text-ink/60">{run.rows} rows processed</div>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
