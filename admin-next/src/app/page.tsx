"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getAuthToken } from "@/lib/api";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    if (getAuthToken()) router.replace("/dashboard");
    else router.replace("/login");
  }, [router]);
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
    </div>
  );
}
