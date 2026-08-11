"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { apiGet, apiPost } from "@/lib/api";

export default function OTPCashPage() {
  const router = useRouter();
  const [quantity, setQuantity] = useState(1);
  const [settings, setSettings] = useState<{
    subscription_price: number;
    subscription_currency: string;
    subscription_duration: number;
  } | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [created, setCreated] = useState<{ code: string; id: string }[]>([]);

  useEffect(() => {
    apiGet<{
      subscription_price: number;
      subscription_currency: string;
      subscription_duration: number;
    }>("/otp/cash-payment/")
      .then(setSettings)
      .catch(() => setSettings({ subscription_price: 5000, subscription_currency: "UZS", subscription_duration: 30 }));
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    setCreated([]);
    try {
      const data = await apiPost<{ created: { code: string; id: string }[]; message: string }>(
        "/otp/cash-payment/",
        { quantity }
      );
      setCreated(data.created);
      if (data.created.length === 1) {
        router.push(`/dashboard/otp/${data.created[0].id}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  const price = settings?.subscription_price ?? 5000;
  const total = price * quantity;

  return (
    <div>
      <div className="mb-8 flex items-center gap-4">
        <Link href="/dashboard/otp" className="text-slate-600 hover:text-slate-900">
          ← OTP коды
        </Link>
        <h1 className="text-2xl font-bold text-slate-800">Наличный платёж</h1>
      </div>
      <div className="card max-w-md">
        {settings && (
          <p className="mb-4 text-sm text-slate-600">
            Цена за билет: {settings.subscription_price.toLocaleString()} {settings.subscription_currency} · 
            Длительность: {settings.subscription_duration} мин
          </p>
        )}
        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</div>
          )}
          <div>
            <label htmlFor="qty" className="label">Количество билетов (1–10)</label>
            <input
              id="qty"
              type="number"
              min={1}
              max={10}
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value) || 1)}
              className="input"
            />
          </div>
          <p className="text-lg font-semibold">Итого: {total.toLocaleString()} UZS</p>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "Создание…" : "Создать OTP коды"}
          </button>
        </form>
        {created.length > 1 && (
          <div className="mt-6 rounded-lg bg-emerald-50 p-4">
            <p className="font-medium text-emerald-800">Создано кодов: {created.length}</p>
            <ul className="mt-2 space-y-1 font-mono text-sm">
              {created.map((c) => (
                <li key={c.id}>
                  {c.code} — <Link href={`/dashboard/otp/${c.id}`} className="text-emerald-600 hover:underline">открыть</Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
