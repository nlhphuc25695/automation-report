import Link from "next/link";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/clients", label: "Clients" },
  { href: "/templates", label: "Templates" },
  { href: "/schedules", label: "Schedules" },
  { href: "/runs", label: "Runs & Logs" },
  { href: "/settings", label: "Settings" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-sand">
      <div className="absolute inset-0 bg-grid opacity-30" />
      <div className="relative z-10 flex min-h-screen">
        <aside className="w-64 border-r border-ink/10 bg-white/80 backdrop-blur">
          <div className="p-6">
            <div className="font-display text-xl uppercase tracking-[0.2em] text-moss">
              Report
            </div>
            <div className="text-sm text-ink/60">Automation Suite</div>
          </div>
          <nav className="space-y-2 px-4">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block rounded-xl px-4 py-3 text-sm font-semibold tracking-wide text-ink/70 transition hover:bg-clay/60 hover:text-ink"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>
        <main className="flex-1 px-10 py-8">{children}</main>
      </div>
    </div>
  );
}
