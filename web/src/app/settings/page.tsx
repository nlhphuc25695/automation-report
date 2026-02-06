import { AppShell } from "@/components/AppShell";

export default function SettingsPage() {
  return (
    <AppShell>
      <div>
        <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Settings</div>
        <h1 className="mt-2 font-display text-4xl text-ink">Environment & Secrets</h1>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">BigQuery</div>
          <div className="mt-4 text-sm text-ink/60">Project: {process.env.GCP_PROJECT_ID || "Not configured"}</div>
          <div className="text-sm text-ink/60">Dataset: ads_reporting</div>
        </div>
        <div className="rounded-3xl border border-ink/10 bg-white/90 p-6 shadow-sm">
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Secrets Manager</div>
          <div className="mt-4 text-sm text-ink/60">Meta: meta_ads_token</div>
          <div className="text-sm text-ink/60">Google Ads: google_ads_token</div>
          <div className="text-sm text-ink/60">TikTok: tiktok_ads_token</div>
        </div>
      </div>
    </AppShell>
  );
}
