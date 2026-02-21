"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiPost, setAuthToken } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await apiPost<{ token: string; user: { username: string; role: string } }>(
        "/auth/login/",
        { username, password }
      );
      setAuthToken(data.token);
      router.replace("/dashboard");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка входа");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-900 p-4">
      <div className="w-full max-w-md">
        <div className="rounded-2xl border border-slate-700/50 bg-slate-800/80 p-8 shadow-2xl backdrop-blur">
          <div className="mb-8 text-center">
            <h1 className="text-2xl font-bold text-white">ComeBack Admin</h1>
            <p className="mt-1 text-slate-400">Войдите в панель управления</p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="rounded-lg bg-red-500/20 px-3 py-2 text-sm text-red-200">
                {error}
              </div>
            )}
            <div>
              <label htmlFor="username" className="label text-slate-300">
                Логин
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input border-slate-600 bg-slate-700/50 text-white placeholder-slate-500"
                placeholder="admin"
                required
                autoComplete="username"
              />
            </div>
            <div>
              <label htmlFor="password" className="label text-slate-300">
                Пароль
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input border-slate-600 bg-slate-700/50 text-white placeholder-slate-500"
                placeholder="••••••••"
                required
                autoComplete="current-password"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3"
            >
              {loading ? "Вход..." : "Войти"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
