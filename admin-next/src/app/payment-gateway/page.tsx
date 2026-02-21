"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function PaymentGatewayRedirectPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/dashboard/payment-gateway");
  }, [router]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-slate-50">
      <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      <p className="text-slate-600">Переход к эквайрингу…</p>
    </div>
  );
}
