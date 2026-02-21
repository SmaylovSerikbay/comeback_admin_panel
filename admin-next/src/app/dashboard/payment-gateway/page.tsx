"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet } from "@/lib/api";

type Transaction = {
  order_id: string;
  amount: number;
  currency: string;
  status: string;
  status_display: string;
  description: string;
  unity_user_id: string;
  unity_session_id: string;
  payment_id: string | null;
  merchant_id: string;
  created_at: string;
  updated_at: string;
  paid_at: string | null;
};

type Stats = {
  total: number;
  pending: number;
  success: number;
  failed: number;
  total_amount: number;
};

export default function PaymentGatewayPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet<{
      stats: Stats;
      transactions: Transaction[];
      total: number;
      page: number;
      per_page: number;
    }>(`/payment-gateway/?page=${page}`)
      .then((d) => {
        setStats(d.stats);
        setTransactions(d.transactions);
        setTotal(d.total);
      })
      .catch(() => setStats(null))
      .finally(() => setLoading(false));
  }, [page]);

  if (loading && !stats) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Эквайринг (FreedomPay)</h1>
        <Link href="/dashboard/payment-gateway/test" className="btn-primary">
          Тестовый платёж
        </Link>
      </div>

      {stats && (
        <div className="mb-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div className="card">
            <p className="text-sm text-slate-500">Всего</p>
            <p className="text-2xl font-bold text-slate-800">{stats.total}</p>
          </div>
          <div className="card">
            <p className="text-sm text-slate-500">Ожидание</p>
            <p className="text-2xl font-bold text-amber-600">{stats.pending}</p>
          </div>
          <div className="card">
            <p className="text-sm text-slate-500">Успешно</p>
            <p className="text-2xl font-bold text-emerald-600">{stats.success}</p>
          </div>
          <div className="card">
            <p className="text-sm text-slate-500">Сумма (успешные)</p>
            <p className="text-2xl font-bold text-slate-800">
              {stats.total_amount.toLocaleString()} UZS
            </p>
          </div>
        </div>
      )}

      <div className="card">
        <p className="mb-4 text-slate-600">Транзакции (всего: {total})</p>
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
          </div>
        ) : transactions.length === 0 ? (
          <p className="text-slate-500">Нет транзакций</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-slate-600">
                  <th className="pb-2 pr-4">Order ID</th>
                  <th className="pb-2 pr-4">Сумма</th>
                  <th className="pb-2 pr-4">Статус</th>
                  <th className="pb-2 pr-4">Дата</th>
                  <th className="pb-2"></th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((t) => (
                  <tr key={t.order_id} className="border-b border-slate-100">
                    <td className="py-2 pr-4 font-mono text-slate-800">{t.order_id}</td>
                    <td className="py-2 pr-4">
                      {t.amount.toLocaleString()} {t.currency}
                    </td>
                    <td className="py-2 pr-4">
                      <span
                        className={`rounded px-2 py-0.5 text-xs ${
                          t.status === "success"
                            ? "bg-emerald-100 text-emerald-700"
                            : t.status === "pending"
                            ? "bg-amber-100 text-amber-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {t.status_display}
                      </span>
                    </td>
                    <td className="py-2 text-slate-500">
                      {new Date(t.created_at).toLocaleString("ru")}
                    </td>
                    <td className="py-2">
                      <Link
                        href={`/dashboard/payment-gateway/transaction/${encodeURIComponent(t.order_id)}`}
                        className="text-emerald-600 hover:underline"
                      >
                        Детали
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {total > 50 && (
          <div className="mt-4 flex gap-2">
            <button
              type="button"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="btn-secondary disabled:opacity-50"
            >
              Назад
            </button>
            <span className="flex items-center text-slate-600">
              Страница {page} из {Math.ceil(total / 50)}
            </span>
            <button
              type="button"
              onClick={() => setPage((p) => p + 1)}
              disabled={page >= Math.ceil(total / 50)}
              className="btn-secondary disabled:opacity-50"
            >
              Вперёд
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
