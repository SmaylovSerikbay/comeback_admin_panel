"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

type DailyRevenue = { date: string; revenue: number };
type StatusStat = { status: string; count: number };
type TopUser = { user_id: string; payment_count: number; total_amount: number; last_payment: string };

export default function StatisticsPage() {
  const [data, setData] = useState<{
    daily_revenue: DailyRevenue[];
    total_payments: number;
    successful_payments: number;
    total_revenue: number;
    status_stats: StatusStat[];
    top_users: TopUser[];
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiGet<{
      daily_revenue: DailyRevenue[];
      total_payments: number;
      successful_payments: number;
      total_revenue: number;
      status_stats: StatusStat[];
      top_users: TopUser[];
    }>("/statistics/")
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
  if (error) {
    return (
      <div className="rounded-lg bg-red-50 p-4 text-red-700">
        {error}
      </div>
    );
  }
  if (!data) return null;

  const { daily_revenue, total_payments, successful_payments, total_revenue, status_stats, top_users } = data;
  const maxRevenue = Math.max(...daily_revenue.map((d) => d.revenue), 1);

  return (
    <div>
      <h1 className="mb-8 text-2xl font-bold text-slate-800">Статистика</h1>
      <div className="mb-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card">
          <p className="text-sm text-slate-500">Всего платежей</p>
          <p className="text-2xl font-bold text-slate-900">{total_payments}</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Успешных</p>
          <p className="text-2xl font-bold text-emerald-600">{successful_payments}</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Общая выручка</p>
          <p className="text-2xl font-bold text-slate-900">{total_revenue.toLocaleString()} UZS</p>
        </div>
      </div>
      <div className="card mb-8">
        <h2 className="mb-4 text-lg font-semibold">Выручка по дням (30 дней)</h2>
        <div className="flex h-48 items-end gap-1">
          {daily_revenue.map((d) => (
            <div
              key={d.date}
              className="min-w-0 flex-1 rounded-t bg-emerald-500/80 transition-all hover:bg-emerald-500"
              style={{ height: `${(d.revenue / maxRevenue) * 100}%` }}
              title={`${d.date}: ${d.revenue.toLocaleString()} UZS`}
            />
          ))}
        </div>
        <div className="mt-2 flex justify-between text-xs text-slate-500">
          <span>{daily_revenue[0]?.date}</span>
          <span>{daily_revenue[daily_revenue.length - 1]?.date}</span>
        </div>
      </div>
      <div className="grid gap-8 lg:grid-cols-2">
        <div className="card">
          <h2 className="mb-4 text-lg font-semibold">По статусам</h2>
          <ul className="space-y-2">
            {status_stats.map((s) => (
              <li key={s.status} className="flex justify-between text-sm">
                <span className="text-slate-600">{s.status}</span>
                <span className="font-medium">{s.count}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h2 className="mb-4 text-lg font-semibold">Топ пользователей (по сумме)</h2>
          {top_users.length === 0 ? (
            <p className="text-slate-500">Нет данных</p>
          ) : (
            <ul className="space-y-2 text-sm">
              {top_users.map((u) => (
                <li key={u.user_id} className="flex justify-between">
                  <span className="font-mono text-slate-600">{u.user_id}</span>
                  <span>{u.total_amount?.toLocaleString()} UZS</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
