"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { uploadVideo } from "@/lib/api-form";
import ChromaKeyInstructions from "@/components/ChromaKeyInstructions";

const MapPicker = dynamic(
  () => import("@/components/MapPicker").then((m) => m.default),
  { ssr: false, loading: () => <div className="h-80 animate-pulse rounded-lg bg-slate-200" /> }
);

export default function NewVideoPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    if (!file) {
      setError("Выберите видео файл (MP4)");
      return;
    }
    const lat = parseFloat(latitude);
    const lng = parseFloat(longitude);
    if (Number.isNaN(lat) || Number.isNaN(lng)) {
      setError("Введите корректные координаты");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("name", name);
    formData.append("latitude", String(lat));
    formData.append("longitude", String(lng));
    formData.append("video_file", file);
    try {
      await uploadVideo(formData);
      router.push("/dashboard/videos");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка загрузки");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="mb-8 flex items-center gap-4">
        <Link href="/dashboard/videos" className="text-slate-600 hover:text-slate-900">
          ← Видео
        </Link>
        <h1 className="text-2xl font-bold text-slate-800">Добавить видео</h1>
      </div>
      <div className="card max-w-xl">
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
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="lat" className="label">Широта</label>
              <input
                id="lat"
                type="text"
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
          <p className="text-sm text-slate-500">
            Или введите вручную / возьмите координаты на{" "}
            <a href="https://www.latlong.net/" target="_blank" rel="noopener noreferrer" className="text-emerald-600 hover:underline">
              latlong.net
            </a>
          </p>
          <ChromaKeyInstructions />
          <div>
            <label htmlFor="file" className="label">Видео (MP4, до 5 MB)</label>
            <input
              id="file"
              type="file"
              accept="video/mp4"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className="input"
              required
            />
          </div>
          <div className="flex gap-3">
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? "Загрузка…" : "Сохранить"}
            </button>
            <Link href="/dashboard/videos" className="btn-secondary">
              Отмена
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
