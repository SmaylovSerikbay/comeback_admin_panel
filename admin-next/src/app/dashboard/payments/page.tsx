"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

type Payment = {
  id: string | number;
  order_id: string;
  amount: number;
  currency: string;
  status: string;
  payment_method: string;
  description: string;
  created_at: string;
  customer_name: string;
  is_otp?: boolean;
  otp_code?: string;
};

export default function PaymentsPage() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [total, setTotal] = useState(0);
  const [statusFilter, setStatusFilter] = useState("all");
  const [dateFilter, setDateFilter] = useState("all");
  const [typeFilter, setTypeFilter] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams();
    if (statusFilter !== "all") params.set("status", statusFilter);
    if (dateFilter !== "all") params.set("date", dateFilter);
    if (typeFilter !== "all") params.set("type", typeFilter);
    apiGet<{ payments: Payment[]; total: number }>(`/payments/?${params}`)
      .then((d) => {
        setPayments(d.payments);
        setTotal(d.total);
      })
      .finally(() => setLoading(false));
  }, [statusFilter, dateFilter, typeFilter]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="mb-6 text-xl font-bold text-slate-800 sm:mb-8 sm:text-2xl">Платежи</h1>
      <div className="mb-4 flex flex-wrap gap-3 sm:mb-6 sm:gap-4">
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input w-auto"
        >
          <option value="all">Все статусы</option>
          <option value="success">Успешно</option>
          <option value="pending">Ожидание</option>
          <option value="failed">Ошибка</option>
        </select>
        <select
          value={dateFilter}
          onChange={(e) => setDateFilter(e.target.value)}
          className="input w-auto"
        >
          <option value="all">Все даты</option>
          <option value="today">Сегодня</option>
          <option value="week">Неделя</option>
          <option value="month">Месяц</option>
        </select>
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="input w-auto"
        >
          <option value="all">Все типы</option>
          <option value="online">Онлайн</option>
          <option value="cash">Наличные (OTP)</option>
        </select>
      </div>
      <div className="card overflow-hidden p-4 sm:p-6">
        <p className="mb-4 text-sm text-slate-600 sm:text-base">Всего: {total}</p>
        {payments.length === 0 ? (
          <p className="text-slate-500">Нет платежей</p>
        ) : (
          <div className="table-responsive">
            <table className="w-full min-w-[600px] text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-slate-600">
                  <th className="pb-2 pr-4">Заказ / OTP</th>
                  <th className="pb-2 pr-4">Сумма</th>
                  <th className="pb-2 pr-4">Тип</th>
                  <th className="pb-2 pr-4">Статус</th>
                  <th className="pb-2">Дата</th>
                </tr>
              </thead>
              <tbody>
                {payments.map((p) => (
                  <tr key={String(p.id)} className="border-b border-slate-100">
                    <td className="py-2 pr-4">
                      <span className="font-mono">{p.order_id}</span>
                      {p.is_otp && (
                        <span className="ml-2 rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-600">
                          OTP
                        </span>
                      )}
                    </td>
                    <td className="py-2 pr-4">
                      {p.amount.toLocaleString()} {p.currency}
                    </td>
                    <td className="py-2 pr-4">{p.payment_method === "cash_otp" ? "Наличные" : "Онлайн"}</td>
                    <td className="py-2 pr-4">
                      <span
                        className={`rounded px-2 py-0.5 text-xs ${
                          p.status === "success" || p.status === "completed"
                            ? "bg-emerald-100 text-emerald-700"
                            : p.status === "pending"
                            ? "bg-amber-100 text-amber-700"
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
