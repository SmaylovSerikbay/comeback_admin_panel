function getApiBaseForForm(): string {
  if (typeof window === "undefined") {
    return process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";
  }
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  const host = window.location.hostname;
  const protocol = window.location.protocol;
  return `${protocol}//${host}:8000/api`;
}

export function getAuthTokenForForm(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("admin_token");
}

export function getApiBase() {
  return getApiBaseForForm();
}

export async function uploadVideo(formData: FormData): Promise<{ id: string; name: string; objectURL: string; x: number; y: number }> {
  const base = getApiBase();
  const t = getAuthTokenForForm();
  const res = await fetch(`${base}/videos/create/`, {
    method: "POST",
    headers: t ? { Authorization: `Token ${t}` } : {},
    body: formData,
  });
  const text = await res.text();
  let data: { id?: string; name?: string; objectURL?: string; x?: number; y?: number; error?: string };
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(text || res.statusText);
  }
  if (!res.ok) throw new Error(data.error || text);
  return {
    id: data.id!,
    name: data.name!,
    objectURL: data.objectURL!,
    x: data.x ?? 0,
    y: data.y ?? 0,
  };
}
