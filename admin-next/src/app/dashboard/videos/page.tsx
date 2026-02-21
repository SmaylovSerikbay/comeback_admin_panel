"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet, apiDelete } from "@/lib/api";

type Video = { id: string; name: string; objectURL: string; x: number; y: number };

export default function VideosPage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [total, setTotal] = useState(0);
  const [userRole, setUserRole] = useState("");
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState<string | null>(null);

  function load() {
    apiGet<{ videos: Video[]; total: number; user_role: string }>("/videos/")
      .then((d) => {
        setVideos(d.videos);
        setTotal(d.total);
        setUserRole(d.user_role);
      })
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  function handleDelete(id: string, name: string) {
    if (!confirm(`Удалить видео «${name}»?`)) return;
    setDeleting(id);
    apiDelete(`/videos/${id}/delete/`)
      .then(() => load())
      .catch((e) => alert(e.message))
      .finally(() => setDeleting(null));
  }

  const isAdmin = userRole === "admin";

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
        <h1 className="text-2xl font-bold text-slate-800">Видео</h1>
        {isAdmin && (
          <Link href="/dashboard/videos/new" className="btn-primary">
            + Добавить видео
          </Link>
        )}
      </div>
      <p className="mb-6 text-slate-600">Всего: {total}</p>
      <div className="card">
        {videos.length === 0 ? (
          <p className="text-slate-500">Нет видео</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-slate-600">
                  <th className="pb-2 pr-4">Название</th>
                  <th className="pb-2 pr-4">Координаты</th>
                  <th className="pb-2 pr-4">Ссылка</th>
                  {isAdmin && <th className="pb-2">Действия</th>}
                </tr>
              </thead>
              <tbody>
                {videos.map((v) => (
                  <tr key={v.id} className="border-b border-slate-100">
                    <td className="py-2 pr-4 font-medium">{v.name}</td>
                    <td className="py-2 pr-4 text-slate-600">
                      {v.x}, {v.y}
                    </td>
                    <td className="py-2 pr-4">
                      <a
                        href={v.objectURL}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-emerald-600 hover:underline"
                      >
                        Открыть
                      </a>
                    </td>
                    {isAdmin && (
                      <td className="py-2">
                        <Link
                          href={`/dashboard/videos/${v.id}/edit`}
                          className="text-slate-600 hover:text-slate-900 mr-3"
                        >
                          Изменить
                        </Link>
                        <button
                          type="button"
                          disabled={deleting === v.id}
                          onClick={() => handleDelete(v.id, v.name)}
                          className="text-red-600 hover:text-red-700 disabled:opacity-50"
                        >
                          {deleting === v.id ? "…" : "Удалить"}
                        </button>
                      </td>
                    )}
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
