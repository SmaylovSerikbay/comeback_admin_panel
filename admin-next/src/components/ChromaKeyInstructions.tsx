"use client";

export default function ChromaKeyInstructions() {
  return (
    <div className="rounded-lg border border-emerald-200 bg-emerald-50/80 p-4">
      <h3 className="mb-2 text-sm font-semibold text-emerald-900">
        Хромакей (зелёный экран) для AR
      </h3>
      <ul className="space-y-1 text-sm text-emerald-800">
        <li>
          <strong>Цвет фона:</strong> используйте зелёный экран точно цвета{" "}
          <span
            className="inline-block rounded px-1.5 py-0.5 font-mono text-white"
            style={{ backgroundColor: "#00b23f" }}
          >
            #00b23f
          </span>{" "}
          (RGB: 0, 178, 63). Unity сделает этот цвет прозрачным в AR.
        </li>
        <li>
          <strong>Освещение:</strong> равномерно, без теней на фоне.
        </li>
        <li>
          <strong>Одежда:</strong> не используйте зелёные оттенки.
        </li>
        <li>
          <strong>Формат:</strong> MP4 H.264, до 5 МБ.
        </li>
      </ul>
    </div>
  );
}
