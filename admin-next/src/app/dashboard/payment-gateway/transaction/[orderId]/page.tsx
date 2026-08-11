"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { apiGet } from "@/lib/api";

type Transaction = {
  order_id: string;
  gateway: string;
  amount: number;
  currency: string;
  status: string;
  status_display: string;
  description: string;
  unity_user_id: string;
  unity_session_id: string;
  payment_id: string | null;
  merchant_id: string;
  milliy_transaction_id: string | null;
  created_at: string;
  updated_at: string;
  paid_at: string | null;
};

type Callback = {
  callback_type: string;
  raw_data: Record<string, unknown>;
  processed: boolean;
  created_at: string;
};

export default function TransactionDetailPage() {
  const params = useParams();
  const orderId = params.orderId as string;
  const [transaction, setTransaction] = useState<Transaction | null>(null);
  const [callbacks, setCallbacks] = useState<Callback[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiGet<{ transaction: Transaction; callbacks: Callback[] }>(
      `/payment-gateway/transaction/${encodeURIComponent(orderId)}/`
    )
      .then((d) => {
        setTransaction(d.transaction);
        setCallbacks(d.callbacks);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Ошибка"))
      .finally(() => setLoading(false));
  }, [orderId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }

  if (error || !transaction) {
    return (
      <div>
        <Link href="/dashboard/payment-gateway" className="text-slate-600 hover:text-slate-900">
          ← Эквайринг
        </Link>
        <p className="mt-4 text-red-600">{error || "Транзакция не найдена"}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex items-center gap-4">
        <Link href="/dashboard/payment-gateway" className="text-slate-600 hover:text-slate-900">
          ← Эквайринг
        </Link>
      </div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Транзакция {transaction.order_id}</h1>

      <div className="card mb-6">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Данные</h2>
        <dl className="grid gap-2 text-sm sm:grid-cols-2">
          <dt className="text-slate-500">Order ID</dt>
          <dd className="font-mono">{transaction.order_id}</dd>
          <dt className="text-slate-500">Шлюз</dt>
          <dd>{transaction.gateway === "milliy" ? "Milliy Ecom" : "FreedomPay"}</dd>
          <dt className="text-slate-500">Сумма</dt>
          <dd>
            {transaction.amount.toLocaleString()} {transaction.currency}
          </dd>
          <dt className="text-slate-500">Статус</dt>
          <dd>
            <span
              className={`rounded px-2 py-0.5 text-xs ${
                transaction.status === "success"
                  ? "bg-emerald-100 text-emerald-700"
                  : transaction.status === "pending"
                  ? "bg-amber-100 text-amber-700"
                  : "bg-red-100 text-red-700"
              }`}
            >
              {transaction.status_display}
            </span>
          </dd>
          <dt className="text-slate-500">Описание</dt>
          <dd>{transaction.description || "—"}</dd>
          <dt className="text-slate-500">Unity User ID</dt>
          <dd>{transaction.unity_user_id || "—"}</dd>
          <dt className="text-slate-500">Payment ID</dt>
          <dd>{transaction.payment_id || "—"}</dd>
          <dt className="text-slate-500">Создан</dt>
          <dd>{new Date(transaction.created_at).toLocaleString("ru")}</dd>
          {transaction.paid_at && (
            <>
              <dt className="text-slate-500">Оплачен</dt>
              <dd>{new Date(transaction.paid_at).toLocaleString("ru")}</dd>
            </>
          )}
        </dl>
      </div>

      {callbacks.length > 0 && (
        <div className="card">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Коллбэки</h2>
          <div className="space-y-4">
            {callbacks.map((c, i) => (
              <div key={i} className="rounded border border-slate-200 bg-slate-50 p-3 text-sm">
                <p className="mb-1 font-medium text-slate-700">
                  {c.callback_type} — {new Date(c.created_at).toLocaleString("ru")}{" "}
                  {c.processed && <span className="text-emerald-600">(обработан)</span>}
                </p>
                <pre className="overflow-x-auto whitespace-pre-wrap break-words text-xs text-slate-600">
                  {JSON.stringify(c.raw_data, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
