"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { apiGet } from "@/lib/api";

export default function OTPDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [otp, setOtp] = useState<{
    code: string;
    amount: number;
    quantity: number;
    currency: string;
    status: string;
    created_at: string;
    created_by: string;
    used_at: string | null;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet<{
      code: string;
      amount: number;
      quantity: number;
      currency: string;
      status: string;
      created_at: string;
      created_by: string;
      used_at: string | null;
    }>(`/otp/${id}/`)
      .then(setOtp)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }
  if (!otp) {
    return (
      <div className="rounded-lg bg-red-50 p-4 text-red-700">OTP не найден</div>
    );
  }

  return (
    <div>
      <div className="mb-8 flex items-center gap-4">
        <Link href="/dashboard/otp" className="text-slate-600 hover:text-slate-900">
          ← OTP коды
        </Link>
        <h1 className="text-2xl font-bold text-slate-800">OTP {otp.code}</h1>
      </div>
      <div className="card max-w-lg">
        <div className="mb-4 text-4xl font-mono font-bold tracking-widest text-emerald-600">
          {otp.code}
        </div>
        <dl className="space-y-2 text-sm">
          <div className="flex justify-between">
            <dt className="text-slate-500">Сумма</dt>
            <dd>{otp.amount.toLocaleString()} {otp.currency}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-slate-500">Количество / Длительность</dt>
            <dd>{otp.quantity}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-slate-500">Статус</dt>
            <dd>
              <span
                className={`rounded px-2 py-0.5 text-xs ${
                  otp.status === "active"
                    ? "bg-amber-100 text-amber-700"
                    : otp.status === "used"
                    ? "bg-emerald-100 text-emerald-700"
                    : "bg-slate-100 text-slate-600"
                }`}
              >
                {otp.status}
              </span>
            </dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-slate-500">Создал</dt>
            <dd>{otp.created_by}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-slate-500">Создан</dt>
            <dd>{new Date(otp.created_at).toLocaleString("ru")}</dd>
          </div>
          {otp.used_at && (
            <div className="flex justify-between">
              <dt className="text-slate-500">Использован</dt>
              <dd>{new Date(otp.used_at).toLocaleString("ru")}</dd>
            </div>
          )}
        </dl>
      </div>
    </div>
  );
}
