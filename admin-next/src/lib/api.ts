// В браузере: тот же хост (nginx проксирует /api/ на Django). Порт 8000 недоступен снаружи.
function getApiBase(): string {
  if (typeof window === "undefined") {
    return process.env.NEXT_PUBLIC_API_URL || (process.env.API_UPSTREAM || "http://web:8000") + "/api";
  }
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  // Относительный /api — запрос идёт на тот же origin, nginx отдаёт в web:8000
  return "/api";
}
const API_BASE = getApiBase();

/** Базовый URL бэкенда Django (без /api) — для редиректа на payment-gateway и т.п. */
export function getBackendOrigin(): string {
  if (typeof window === "undefined") {
    const base = process.env.NEXT_PUBLIC_API_URL || (process.env.API_UPSTREAM || "http://web:8000") + "/api";
    return base.replace(/\/api\/?$/, "") || base;
  }
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/api\/?$/, "");
  }
  return `${window.location.protocol}//${window.location.host}`;
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
