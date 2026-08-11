"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { apiGet, getAuthToken, setAuthToken } from "@/lib/api";

type User = { id: number; username: string; email: string; role: string };

const nav = [
  { href: "/dashboard", label: "Дашборд", icon: "📊" },
  { href: "/dashboard/videos", label: "Видео", icon: "🎬", admin: true },
  { href: "/dashboard/payments", label: "Платежи", icon: "💳" },
  { href: "/dashboard/otp", label: "OTP коды", icon: "🔑" },
  { href: "/dashboard/subscription", label: "Подписка", icon: "⚙️", admin: true },
  { href: "/dashboard/statistics", label: "Статистика", icon: "📈", admin: true },
  { href: "/dashboard/payment-gateway", label: "Эквайринг", icon: "🏦" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (!getAuthToken()) {
      router.replace("/login");
      return;
    }
    apiGet<{ user: User }>("/auth/me/")
      .then((d) => setUser(d.user))
      .catch(() => {
        setAuthToken(null);
        router.replace("/login");
      })
      .finally(() => setLoading(false));
  }, [router]);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  function logout() {
    setAuthToken(null);
    router.replace("/login");
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }

  const isAdmin = user?.role === "admin";
  const links = nav.filter((l) => !l.admin || isAdmin);

  return (
    <div className="flex min-h-screen">
      {/* Оверлей при открытом меню на мобильных */}
      <button
        type="button"
        aria-label="Закрыть меню"
        className={`fixed inset-0 z-30 bg-slate-900/50 md:hidden ${menuOpen ? "" : "pointer-events-none invisible"}`}
        onClick={() => setMenuOpen(false)}
      />

      <aside
        className={`fixed inset-y-0 left-0 z-40 w-64 transform border-r border-slate-200 bg-white shadow-sm transition-transform duration-200 ease-out md:translate-x-0 ${
          menuOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex h-14 items-center justify-between border-b border-slate-200 px-4 md:px-6">
          <Link href="/dashboard" className="text-lg font-semibold text-slate-800">
            ComeBack Admin
          </Link>
          <button
            type="button"
            aria-label="Закрыть меню"
            className="rounded p-2 text-slate-500 hover:bg-slate-100 md:hidden"
            onClick={() => setMenuOpen(false)}
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <nav className="space-y-0.5 overflow-y-auto p-4" style={{ maxHeight: "calc(100vh - 8rem)" }}>
          {links.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  active
                    ? "bg-emerald-50 text-emerald-700"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                }`}
              >
                <span>{item.icon}</span>
                {item.label}
              </Link>
            );
          })}
        </nav>
        <div className="absolute bottom-0 left-0 right-0 border-t border-slate-200 bg-white p-4">
          <div className="flex items-center justify-between">
            <span className="truncate text-sm text-slate-500">{user?.username}</span>
            <span className="shrink-0 rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
              {user?.role === "admin" ? "Админ" : "Кассир"}
            </span>
          </div>
          <button
            type="button"
            onClick={logout}
            className="mt-2 text-sm text-slate-500 hover:text-slate-700"
          >
            Выйти
          </button>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Верхняя полоса на мобильных: логотип + кнопка меню */}
        <header className="sticky top-0 z-20 flex h-14 shrink-0 items-center gap-3 border-b border-slate-200 bg-white px-4 md:hidden">
          <button
            type="button"
            aria-label="Открыть меню"
            className="rounded p-2 text-slate-600 hover:bg-slate-100"
            onClick={() => setMenuOpen(true)}
          >
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <span className="font-semibold text-slate-800">ComeBack Admin</span>
        </header>

        <main className="min-w-0 flex-1 md:pl-64">
          <div className="min-h-screen bg-slate-50 p-4 sm:p-6 md:p-8">{children}</div>
        </main>
      </div>
    </div>
  );
}
