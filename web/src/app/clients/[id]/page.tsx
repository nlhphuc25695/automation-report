import { AppShell } from "@/components/AppShell";

export default function ClientDetailPage() {
  return (
    <AppShell>
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Client</div>
          <h1 className="mt-2 font-display text-4xl text-ink">Client A</h1>
        </div>
        <button className="rounded-full bg-ember px-6 py-3 text-sm font-semibold text-white">
          Run client
        </button>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm lg:col-span-2">
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Configuration</div>
          <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
            {[
              { label: "Objective", value: "Ecom" },
              { label: "Platforms", value: "Meta, Google, TikTok" },
              { label: "Drive Folder", value: "drive_folder_id" },
              { label: "Metabase Embed", value: "Connected" },
            ].map((item) => (
              <div key={item.label}>
                <div className="text-xs uppercase tracking-[0.3em] text-ink/40">{item.label}</div>
                <div className="mt-2 text-sm font-semibold text-ink">{item.value}</div>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Latest Run</div>
          <div className="mt-4 text-2xl font-display text-ink">Feb 2026</div>
          <div className="mt-2 text-sm text-ink/60">12,540 rows processed</div>
          <button className="mt-6 w-full rounded-full border border-ink/20 px-4 py-2 text-sm font-semibold">
            View report
          </button>
        </div>
      </div>

      <div className="mt-8 rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
        <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Metabase Dashboard</div>
        <div className="mt-4 text-sm text-ink/60">Embed URL will appear here once configured.</div>
      </div>
    </AppShell>
  );
}
