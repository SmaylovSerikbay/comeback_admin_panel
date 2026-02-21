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
      <aside className="fixed inset-y-0 left-0 z-40 w-64 border-r border-slate-200 bg-white shadow-sm">
        <div className="flex h-16 items-center border-b border-slate-200 px-6">
          <Link href="/dashboard" className="text-lg font-semibold text-slate-800">
            ComeBack Admin
          </Link>
        </div>
        <nav className="space-y-0.5 p-4">
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
        <div className="absolute bottom-0 left-0 right-0 border-t border-slate-200 p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-500">{user?.username}</span>
            <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
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
      <main className="flex-1 pl-64">
        <div className="min-h-screen bg-slate-50 p-8">{children}</div>
      </main>
    </div>
  );
}
