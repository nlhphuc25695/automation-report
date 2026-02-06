import { AppShell } from "@/components/AppShell";

const templates = [
  { name: "Ecom", focus: "Revenue, ROAS, Orders", color: "bg-emerald-100" },
  { name: "Lead", focus: "Leads, CPL, Quality", color: "bg-amber-100" },
  { name: "Branding", focus: "Reach, Impressions, CPM", color: "bg-indigo-100" },
  { name: "Social", focus: "Engagement, ER, Community", color: "bg-rose-100" },
];

export default function TemplatesPage() {
  return (
    <AppShell>
      <div>
        <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Templates</div>
        <h1 className="mt-2 font-display text-4xl text-ink">Objective Templates</h1>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
        {templates.map((template) => (
          <div key={template.name} className="rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
            <div className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${template.color}`}>
              {template.name}
            </div>
            <div className="mt-4 text-lg font-semibold text-ink">{template.focus}</div>
            <p className="mt-2 text-sm text-ink/60">
              Template includes Google Sheet tabs + Slide outline + KPI sections aligned to the objective.
            </p>
            <button className="mt-6 rounded-full border border-ink/20 px-4 py-2 text-sm font-semibold">
              Preview
            </button>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
