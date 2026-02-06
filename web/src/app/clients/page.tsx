import Link from "next/link";
import { AppShell } from "@/components/AppShell";

const clients = [
  { id: "client-a", name: "Client A", objective: "Ecom", platforms: "Meta, Google, TikTok", status: "Healthy" },
  { id: "client-b", name: "Client B", objective: "Lead", platforms: "Meta, Google", status: "Needs review" },
];

export default function ClientsPage() {
  return (
    <AppShell>
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm uppercase tracking-[0.3em] text-ink/40">Clients</div>
          <h1 className="mt-2 font-display text-4xl text-ink">Client Portfolio</h1>
        </div>
        <button className="rounded-full bg-ember px-6 py-3 text-sm font-semibold text-white">
          Add client
        </button>
      </div>

      <div className="mt-8 space-y-4">
        {clients.map((client) => (
          <Link
            key={client.id}
            href={`/clients/${client.id}`}
            className="block rounded-2xl border border-ink/10 bg-white/90 p-6 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="text-lg font-semibold text-ink">{client.name}</div>
                <div className="text-sm text-ink/60">
                  {client.objective} | {client.platforms}
                </div>
              </div>
              <div className="rounded-full bg-ink/10 px-3 py-1 text-xs font-semibold text-ink">
                {client.status}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </AppShell>
  );
}
