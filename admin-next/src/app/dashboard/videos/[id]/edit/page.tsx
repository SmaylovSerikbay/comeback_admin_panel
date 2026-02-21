"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { apiGet, apiPut } from "@/lib/api";
import { getApiBase, getAuthTokenForForm } from "@/lib/api-form";
import ChromaKeyInstructions from "@/components/ChromaKeyInstructions";

const MapPicker = dynamic(
  () => import("@/components/MapPicker").then((m) => m.default),
  { ssr: false, loading: () => <div className="h-80 animate-pulse rounded-lg bg-slate-200" /> }
);

export default function EditVideoPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const [name, setName] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    apiGet<{ name: string; x: number; y: number }>(`/videos/${id}/`)
      .then((d) => {
        setName(d.name);
        setLatitude(String(d.x));
        setLongitude(String(d.y));
      })
      .catch((e) => setError(e.message))
      .finally(() => setFetching(false));
  }, [id]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    const lat = parseFloat(latitude);
    const lng = parseFloat(longitude);
    if (Number.isNaN(lat) || Number.isNaN(lng)) {
      setError("Введите корректные координаты");
      return;
    }
    setLoading(true);
    try {
      if (file) {
        const formData = new FormData();
        formData.append("name", name);
        formData.append("latitude", String(lat));
        formData.append("longitude", String(lng));
        formData.append("video_file", file);
        const base = getApiBase();
        const t = getAuthTokenForForm();
        const res = await fetch(`${base}/videos/${id}/`, {
          method: "PUT",
          headers: t ? { Authorization: `Token ${t}` } : {},
          body: formData,
        });
        const text = await res.text();
        let data: { error?: string };
        try {
          data = text ? JSON.parse(text) : {};
        } catch {
          throw new Error(text);
        }
        if (!res.ok) throw new Error(data.error || text);
      } else {
        await apiPut(`/videos/${id}/`, {
          name,
          latitude: lat,
          longitude: lng,
        });
      }
      router.push("/dashboard/videos");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  if (fetching) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex flex-col gap-3 sm:mb-8 sm:flex-row sm:items-center sm:gap-4">
        <Link
          href="/dashboard/videos"
          className="inline-flex min-h-[44px] w-fit items-center text-slate-600 hover:text-slate-900"
        >
          ← Видео
        </Link>
        <h1 className="text-xl font-bold text-slate-800 sm:text-2xl">Редактировать видео</h1>
      </div>
      <div className="card w-full max-w-xl p-4 sm:p-6">
        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</div>
          )}
          <div>
            <label htmlFor="name" className="label">Название</label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input"
              required
            />
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="lat" className="label">Широта</label>
              <input
                id="lat"
                type="text"
                inputMode="decimal"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                className="input"
                placeholder="41.2995"
                required
              />
            </div>
            <div>
              <label htmlFor="lng" className="label">Долгота</label>
              <input
                id="lng"
                type="text"
                inputMode="decimal"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                className="input"
                placeholder="69.2401"
                required
              />
            </div>
          </div>
          <MapPicker
            latitude={latitude}
            longitude={longitude}
            onLatitudeChange={setLatitude}
            onLongitudeChange={setLongitude}
          />
          <ChromaKeyInstructions />
          <div>
            <label htmlFor="file" className="label">Новое видео (необязательно)</label>
            <input
              id="file"
              type="file"
              accept="video/mp4"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className="input min-h-[44px] py-2"
            />
          </div>
          <div className="flex flex-col gap-3 sm:flex-row sm:gap-3">
            <button type="submit" disabled={loading} className="btn-primary min-h-[44px] flex-1 sm:flex-none">
              {loading ? "Сохранение…" : "Сохранить"}
            </button>
            <Link href="/dashboard/videos" className="btn-secondary inline-flex min-h-[44px] flex-1 items-center justify-center text-center sm:flex-none">
              Отмена
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
