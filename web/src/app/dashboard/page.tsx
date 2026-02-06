import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Overview</div>
          <h1 className="mt-2 font-display text-4xl text-ink">Monthly Reporting Control</h1>
        </div>
        <button className="rounded-full bg-ember px-6 py-3 text-sm font-semibold text-white">
          Run now
        </button>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-3">
        <StatCard title="Clients" value="12" hint="8 running this month" />
        <StatCard title="Success" value="92%" hint="Last 30 days" />
        <StatCard title="Alerts" value="2" hint="Needs attention" />
      </div>

      <div className="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-[2fr_1fr]">
        <div className="rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Latest Runs</div>
            <div className="text-xs text-ink/50">Feb 2026</div>
          </div>
          <div className="mt-6 space-y-4">
            {[
              { name: "Client A", status: "Success", rows: "12,540" },
              { name: "Client B", status: "Partial", rows: "8,210" },
              { name: "Client C", status: "Failed", rows: "0" },
            ].map((item) => (
              <div key={item.name} className="flex items-center justify-between rounded-2xl border border-ink/10 px-4 py-3">
                <div>
                  <div className="font-semibold text-ink">{item.name}</div>
                  <div className="text-xs text-ink/50">{item.rows} rows</div>
                </div>
                <div className="rounded-full bg-ink/10 px-3 py-1 text-xs font-semibold text-ink">
                  {item.status}
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Metabase</div>
          <div className="mt-4 text-lg font-display text-ink">Embeddable Dashboard</div>
          <p className="mt-3 text-sm text-ink/60">
            Use Metabase embed URLs per client to provide a live BI experience. This panel can be configured to
            show the current month for a selected client.
          </p>
          <button className="mt-6 rounded-full border border-ink/20 px-4 py-2 text-sm font-semibold">
            Configure embed
          </button>
        </div>
      </div>
    </AppShell>
  );
}
