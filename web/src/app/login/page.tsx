export default function LoginPage() {
  return (
    <div className="min-h-screen bg-sand flex items-center justify-center">
      <div className="w-full max-w-md rounded-3xl border border-ink/10 bg-white/90 p-10 shadow-xl">
        <div className="mb-6">
          <div className="font-display text-2xl text-ink">Welcome back</div>
          <div className="text-sm text-ink/60">Sign in to manage client reporting.</div>
        </div>
        <form action="/api/auth/login" method="post" className="space-y-4">
          <label className="block text-sm text-ink/70">
            Email
            <input
              name="email"
              type="email"
              required
              className="mt-2 w-full rounded-xl border border-ink/20 bg-white px-4 py-3 text-sm"
            />
          </label>
          <label className="block text-sm text-ink/70">
            Password
            <input
              name="password"
              type="password"
              required
              className="mt-2 w-full rounded-xl border border-ink/20 bg-white px-4 py-3 text-sm"
            />
          </label>
          <button className="w-full rounded-xl bg-moss px-4 py-3 text-sm font-semibold text-white">
            Sign in
          </button>
        </form>
        <div className="mt-6 text-xs text-ink/50">
          Admin accounts are managed by the agency. Contact an administrator for access.
        </div>
      </div>
    </div>
  );
}
