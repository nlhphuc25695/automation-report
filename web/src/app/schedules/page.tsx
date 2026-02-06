import { AppShell } from "@/components/AppShell";

export default function SchedulesPage() {
  return (
    <AppShell>
      <div>
        <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Schedules</div>
        <h1 className="mt-2 font-display text-4xl text-ink">Monthly Automation</h1>
      </div>

      <div className="mt-8 rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
        <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Primary Schedule</div>
        <div className="mt-4 text-lg font-semibold text-ink">Every 1st of month, 02:00 AM</div>
        <div className="mt-2 text-sm text-ink/60">Timezone: Asia/Ho_Chi_Minh</div>
        <button className="mt-6 rounded-full border border-ink/20 px-4 py-2 text-sm font-semibold">
          Edit schedule
        </button>
      </div>
    </AppShell>
  );
}
