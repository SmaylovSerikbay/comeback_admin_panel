"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet } from "@/lib/api";

type OTP = {
  id: string;
  code: string;
  amount: number;
  quantity: number;
  currency: string;
  status: string;
  created_at: string;
  created_by: string;
};

export default function OTPListPage() {
  const [list, setList] = useState<OTP[]>([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet<{ otp_codes: OTP[]; is_admin: boolean }>("/otp/")
      .then((d) => {
        setList(d.otp_codes);
        setIsAdmin(d.is_admin);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">OTP коды</h1>
        <div className="flex gap-3">
          <Link href="/dashboard/otp/cash" className="btn-primary">
            Наличный платёж
          </Link>
        </div>
      </div>
      <div className="card">
        {list.length === 0 ? (
          <p className="text-slate-500">Нет кодов</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-slate-600">
                  <th className="pb-2 pr-4">Код</th>
                  <th className="pb-2 pr-4">Сумма</th>
                  <th className="pb-2 pr-4">Кол-во / Длительность</th>
                  <th className="pb-2 pr-4">Статус</th>
                  <th className="pb-2 pr-4">Создал</th>
                  <th className="pb-2">Дата</th>
                </tr>
              </thead>
              <tbody>
                {list.map((otp) => (
                  <tr key={otp.id} className="border-b border-slate-100">
                    <td className="py-2 pr-4 font-mono font-semibold">{otp.code}</td>
                    <td className="py-2 pr-4">
                      {otp.amount.toLocaleString()} {otp.currency}
                    </td>
                    <td className="py-2 pr-4">{otp.quantity}</td>
                    <td className="py-2 pr-4">
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
                    </td>
                    <td className="py-2 pr-4">{otp.created_by}</td>
                    <td className="py-2 text-slate-500">
                      {new Date(otp.created_at).toLocaleString("ru")}
                    </td>
                    <td className="py-2">
                      <Link
                        href={`/dashboard/otp/${otp.id}`}
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
      </div>
    </div>
  );
}
