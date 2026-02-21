"use client";

import { useEffect, useState } from "react";
import { apiGet, apiPut } from "@/lib/api";

export default function SubscriptionPage() {
  const [settings, setSettings] = useState<{
    price: number;
    duration_minutes: number;
    currency: string;
    is_active: boolean;
    online_payment_enabled?: boolean;
    otp_enabled?: boolean;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiGet<{
      price: number;
      duration_minutes: number;
      currency: string;
      is_active: boolean;
      online_payment_enabled?: boolean;
      otp_enabled?: boolean;
    }>("/subscription/settings/")
      .then(setSettings)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const [price, setPrice] = useState("");
  const [duration, setDuration] = useState("");
  const [currency, setCurrency] = useState("UZS");
  const [isActive, setIsActive] = useState(true);
  const [onlinePaymentEnabled, setOnlinePaymentEnabled] = useState(true);
  const [otpEnabled, setOtpEnabled] = useState(true);

  useEffect(() => {
    if (settings) {
      setPrice(String(settings.price));
      setDuration(String(settings.duration_minutes));
      setCurrency(settings.currency);
      setIsActive(settings.is_active);
      setOnlinePaymentEnabled(settings.online_payment_enabled ?? true);
      setOtpEnabled(settings.otp_enabled ?? true);
    }
  }, [settings]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setMessage("");
    const p = parseFloat(price);
    const d = parseInt(duration, 10);
    if (Number.isNaN(p) || p <= 0) {
      setError("Введите корректную цену");
      return;
    }
    if (Number.isNaN(d) || d < 1 || d > 1440) {
      setError("Длительность от 1 до 1440 минут");
      return;
    }
    setSaving(true);
    try {
      await apiPut("/subscription/settings/", {
        price: p,
        duration_minutes: d,
        currency,
        is_active: isActive,
        online_payment_enabled: onlinePaymentEnabled,
        otp_enabled: otpEnabled,
      });
      setMessage("Настройки сохранены и синхронизированы с Firebase");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }
  if (error && !settings) {
    return (
      <div className="rounded-lg bg-red-50 p-4 text-red-700">{error}</div>
    );
  }

  return (
    <div>
      <h1 className="mb-8 text-2xl font-bold text-slate-800">Настройки подписки</h1>
      <div className="card max-w-xl">
        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</div>
          )}
          {message && (
            <div className="rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">{message}</div>
          )}
          <div>
            <label htmlFor="price" className="label">Цена (сум)</label>
            <input
              id="price"
              type="number"
              min="0.01"
              step="0.01"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              className="input"
              required
            />
          </div>
          <div>
            <label htmlFor="duration" className="label">Длительность (минут)</label>
            <input
              id="duration"
              type="number"
              min={1}
              max={1440}
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              className="input"
              required
            />
          </div>
          <div>
            <label htmlFor="currency" className="label">Валюта</label>
            <select
              id="currency"
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="input"
            >
              <option value="UZS">UZS</option>
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <input
              id="active"
              type="checkbox"
              checked={isActive}
              onChange={(e) => setIsActive(e.target.checked)}
              className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
            />
            <label htmlFor="active" className="text-sm text-slate-700">
              Подписка активна
            </label>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="mb-3 text-sm font-medium text-slate-700">
              Способы оплаты в Unity-приложении
            </p>
            <div className="flex flex-col gap-2">
              <label className="flex cursor-pointer items-center gap-2">
                <input
                  type="checkbox"
                  checked={onlinePaymentEnabled}
                  onChange={(e) => setOnlinePaymentEnabled(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
                />
                <span className="text-sm text-slate-700">Интернет-оплата (эквайринг) включена</span>
              </label>
              <label className="flex cursor-pointer items-center gap-2">
                <input
                  type="checkbox"
                  checked={otpEnabled}
                  onChange={(e) => setOtpEnabled(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
                />
                <span className="text-sm text-slate-700">OTP (наличные коды) включены</span>
              </label>
            </div>
            <p className="mt-2 text-xs text-slate-500">
              Отключённый способ не будет предлагаться пользователю в приложении. Данные синхронизируются с Firebase.
            </p>
          </div>
          <button type="submit" disabled={saving} className="btn-primary">
            {saving ? "Сохранение…" : "Сохранить"}
          </button>
        </form>
      </div>
    </div>
  );
}
