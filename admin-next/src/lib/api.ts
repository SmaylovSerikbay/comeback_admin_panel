// В браузере: прямой вызов Django на порт 8000 (тот же хост), обходим прокси Next.js
function getApiBase(): string {
  if (typeof window === "undefined") {
    return process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";
  }
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  const host = window.location.hostname;
  const protocol = window.location.protocol;
  return `${protocol}//${host}:8000/api`;
}
const API_BASE = getApiBase();

/** Базовый URL бэкенда Django (без /api) — для редиректа на payment-gateway и т.п. */
export function getBackendOrigin(): string {
  const base = typeof window === "undefined"
    ? (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api")
    : (process.env.NEXT_PUBLIC_API_URL || `${window.location.protocol}//${window.location.hostname}:8000/api`);
  return base.replace(/\/api\/?$/, "") || base;
}

let token: string | null = null;

export function setAuthToken(t: string | null) {
  token = t;
  if (typeof window !== "undefined") {
    if (t) localStorage.setItem("admin_token", t);
    else localStorage.removeItem("admin_token");
  }
}

export function getAuthToken(): string | null {
  if (token) return token;
  if (typeof window !== "undefined") {
    const t = localStorage.getItem("admin_token");
    if (t) token = t;
    return t;
  }
  return null;
}

function headers(extra?: HeadersInit): HeadersInit {
  const h: Record<string, string> = {
    "Content-Type": "application/json",
    ...(extra as Record<string, string>),
  };
  const t = getAuthToken();
  if (t) h["Authorization"] = `Token ${t}`;
  return h;
}

export async function api<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = path.startsWith("http") ? path : `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      ...headers(options.headers as Record<string, string>),
      ...(options.headers as Record<string, string>),
    },
  });
  if (res.status === 401) {
    setAuthToken(null);
    if (typeof window !== "undefined") window.location.href = "/login";
    throw new Error("Unauthorized");
  }
  const text = await res.text();
  let data: T;
  try {
    data = text ? JSON.parse(text) : ({} as T);
  } catch {
    throw new Error(text || res.statusText);
  }
  if (!res.ok) {
    const err = (data as { error?: string }).error || text || res.statusText;
    throw new Error(err);
  }
  return data;
}

export const apiGet = <T>(path: string) => api<T>(path, { method: "GET" });
export const apiPost = <T>(path: string, body?: unknown) =>
  api<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined });
export const apiPut = <T>(path: string, body?: unknown) =>
  api<T>(path, { method: "PUT", body: body ? JSON.stringify(body) : undefined });
export const apiDelete = (path: string) =>
  api<{ success?: boolean }>(path, { method: "DELETE" });
