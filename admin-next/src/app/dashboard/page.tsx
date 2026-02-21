"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

type Stats = {
  today: { payments: number; successful: number; revenue: number };
  week: { payments: number; successful: number; revenue: number };
  month: { payments: number; successful: number; revenue: number };
  all_time: { payments: number; successful: number; revenue: number };
};
type Payment = { id: number; order_id: string; amount: number; currency: string; status: string; created_at: string };

export default function DashboardPage() {
  const [data, setData] = useState<{
    stats: Stats;
    recent_payments: Payment[];
    firebase_status: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiGet<{ stats: Stats; recent_payments: Payment[]; firebase_status: string }>("/dashboard/stats/")
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }
  if (error || !data) {
    return (
      <div className="rounded-lg bg-red-50 p-4 text-red-700">
        {error || "Ошибка загрузки"}
      </div>
    );
  }

  const { stats, recent_payments, firebase_status } = data;
  const cards = [
    { label: "Сегодня", ...stats.today },
    { label: "Неделя", ...stats.week },
    { label: "Месяц", ...stats.month },
    { label: "Всё время", ...stats.all_time },
  ];

  return (
    <div>
      <h1 className="mb-6 text-xl font-bold text-slate-800 sm:mb-8 sm:text-2xl">Дашборд</h1>
      {firebase_status !== "connected" && (
        <div className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800 sm:mb-6 sm:px-4">
          Firebase: {firebase_status === "warning" ? "не настроен" : firebase_status}
        </div>
      )}
      <div className="mb-8 grid gap-4 sm:mb-10 sm:gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((c) => (
          <div key={c.label} className="card p-4 sm:p-6">
            <p className="text-sm font-medium text-slate-500">{c.label}</p>
            <p className="mt-1 text-xl font-bold text-slate-900 sm:text-2xl">{c.payments}</p>
            <p className="text-xs text-slate-600 sm:text-sm">
              Успешно: {c.successful} · {c.revenue.toLocaleString()} UZS
            </p>
          </div>
        ))}
      </div>
      <div className="card overflow-hidden p-4 sm:p-6">
        <h2 className="mb-4 text-base font-semibold sm:text-lg">Последние платежи</h2>
        {recent_payments.length === 0 ? (
          <p className="text-slate-500">Нет платежей</p>
        ) : (
          <div className="table-responsive">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-slate-600">
                  <th className="pb-2 pr-4">Заказ</th>
                  <th className="pb-2 pr-4">Сумма</th>
                  <th className="pb-2 pr-4">Статус</th>
                  <th className="pb-2">Дата</th>
                </tr>
              </thead>
              <tbody>
                {recent_payments.map((p) => (
                  <tr key={p.id} className="border-b border-slate-100">
                    <td className="py-2 pr-4 font-mono">{p.order_id}</td>
                    <td className="py-2 pr-4">{p.amount.toLocaleString()} {p.currency}</td>
                    <td className="py-2 pr-4">
                      <span
                        className={`rounded px-2 py-0.5 text-xs ${
                          p.status === "success"
                            ? "bg-emerald-100 text-emerald-700"
                            : "bg-slate-100 text-slate-600"
                        }`}
                      >
                        {p.status}
                      </span>
                    </td>
                    <td className="py-2 text-slate-500">
                      {new Date(p.created_at).toLocaleString("ru")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
