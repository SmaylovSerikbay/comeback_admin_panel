"use client";

import { useState } from "react";
import Link from "next/link";
import { apiPost } from "@/lib/api";

export default function PaymentGatewayMilliyTestPage() {
  const [amount, setAmount] = useState("1000");
  const [description, setDescription] = useState("Тестовый платёж Milliy");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await apiPost<{ payment_url: string; order_id: string }>(
        "/payment-gateway/test-payment/",
        { amount: parseInt(amount, 10) || 1000, description, gateway: "milliy" }
      );
      window.location.href = data.payment_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка создания платежа");
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="mb-8 flex items-center gap-4">
        <Link href="/dashboard/payment-gateway" className="text-slate-600 hover:text-slate-900">
          ← Эквайринг
        </Link>
      </div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Тестовый платёж (Milliy Ecom)</h1>

      <div className="card max-w-md">
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</div>
          )}
          <div>
            <label htmlFor="amount" className="label">
              Сумма (UZS)
            </label>
            <input
              id="amount"
              type="number"
              min={1000}
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="input"
              required
            />
          </div>
          <div>
            <label htmlFor="description" className="label">
              Описание
            </label>
            <input
              id="description"
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="input"
            />
          </div>
          <div className="flex gap-3">
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? "Перенаправление…" : "Перейти к оплате"}
            </button>
            <Link href="/dashboard/payment-gateway" className="btn-secondary">
              Отмена
            </Link>
          </div>
        </form>
        <p className="mt-4 text-sm text-slate-500">
          Вы будете перенаправлены на страницу оплаты Milliy Ecom (НБУ). Callback вернёт
          статус на сервер автоматически. Минимальная сумма — 1000 UZS.
        </p>
      </div>
    </div>
  );
}
