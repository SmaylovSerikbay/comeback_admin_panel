"use client";

import { useState } from "react";

/** Горизонтальные макеты (баннеры) — рядом с текстом, без кропа по высоте */
const HERO_ASIDE_BANNER = "/images/landing/banner1.png";

/** Вертикальные постеры / слайды AR — только object-contain + достаточная ширина */
const POSTER_MAIN = "/images/landing/slideshow1_ru.png";

const detailTiles = [
  {
    src: "/images/landing/banner2.png",
    alt: "ComeBack — исторические города Узбекистана в AR",
  },
  {
    src: "/images/landing/banner3.png",
    alt: "ComeBack — путешествие во времени",
  },
  {
    src: "/images/landing/slideshow2.png",
    alt: "Дополненная реальность в городах Узбекистана",
  },
] as const;

const gallerySlides = [
  "/images/landing/slideshow1_ru.png",
  "/images/landing/slideshow2.png",
  "/images/landing/ar-slide-2.png",
  "/images/landing/ar-slide-3.png",
  "/images/landing/ar-slide-4.png",
  "/images/landing/ar-slide-5.png",
] as const;

const features = [
  {
    title: "Бухара времён караванов",
    description:
      "Прогуляйтесь по узким улицам древней Бухары, увидьте медресе, базары и кварталы так, как они выглядели сотни лет назад.",
  },
  {
    title: "Самарканд эпохи Великого Шёлкового пути",
    description:
      "Исследуйте площади и мавзолеи Самарканда, почувствуйте масштаб городов, через которые проходили торговцы и путешественники.",
  },
  {
    title: "Живая история Хивы и других городов",
    description:
      "Перемещайтесь во времени, сравнивайте, как выглядели легендарные города Центральной Азии тогда и сейчас.",
  },
];

const steps = [
  "Скачайте приложение ComeBack из магазина приложений.",
  "Выберите город — Бухара, Самарканд, Хива и другие локации.",
  "Наведите камеру и увидьте, какими были эти места в древности.",
];

export default function LandingPage() {
  const [slideIndex, setSlideIndex] = useState(0);
  const nextSlide = () =>
    setSlideIndex((i) => (i + 1) % gallerySlides.length);
  const prevSlide = () =>
    setSlideIndex((i) => (i - 1 + gallerySlides.length) % gallerySlides.length);

  return (
    <div className="flex min-h-screen flex-col bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      <header className="border-b border-slate-800/70">
        <div className="container-page flex h-16 items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/10 ring-1 ring-emerald-500/40">
              <span className="text-lg font-semibold text-emerald-400">
                C
              </span>
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-semibold tracking-tight">ComeBack</span>
              <span className="text-xs text-slate-400">
                Путешествие по древним городам в AR
              </span>
            </div>
          </div>

          <div className="hidden items-center gap-4 text-sm text-slate-300 md:flex">
            <span className="cursor-default text-xs uppercase tracking-[0.18em] text-emerald-400/80">
              BUKHARA / SAMARKAND / KHIVA
            </span>
          </div>
        </div>
      </header>

      <section className="border-b border-slate-800/70 bg-[radial-gradient(circle_at_top,_#22c55e11,_transparent_55%),radial-gradient(circle_at_bottom,_#22c55e22,_transparent_55%)]">
        <div className="container-page grid gap-12 py-14 lg:grid-cols-2 lg:items-center lg:gap-16 lg:py-20">
          <div className="order-2 space-y-6 lg:order-1">
            <p className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/5 px-3 py-1 text-xs font-medium uppercase tracking-[0.18em] text-emerald-300">
              LIVE PROJECT
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.8)]" />
              COMEBACK.UZ
            </p>
            <h1 className="text-balance text-3xl font-semibold tracking-tight text-slate-50 sm:text-4xl md:text-5xl">
              Увидьте Бухару, Самарканд и Хиву
              <span className="text-emerald-400"> такими, какими они были раньше</span>
            </h1>
            <p className="max-w-xl text-pretty text-sm text-slate-300 sm:text-base">
              ComeBack — это AR‑приложение, которое переносит вас в прошлое
              легендарных городов Узбекистана. Смотрите, как выглядели площади,
              улицы и здания много лет назад, прямо на экране вашего телефона.
            </p>
            <div className="flex flex-wrap items-center gap-3">
              <a
                href="#download"
                className="btn-primary"
              >
                Скачать приложение
              </a>
              <a
                href="#download"
                className="btn-outline text-sm"
              >
                Смотреть на карте
              </a>
              <span className="text-xs text-slate-400">
                Для тех, кто любит историю, путешествия и хочет увидеть города
                Узбекистана по‑новому.
              </span>
            </div>
          </div>

          <div className="order-1 flex justify-center lg:order-2 lg:justify-end">
            <figure className="w-full max-w-xl overflow-hidden rounded-2xl border border-emerald-500/35 bg-slate-900/80 shadow-[0_24px_80px_-12px_rgba(16,185,129,0.25)] ring-1 ring-white/5">
              {/* Горизонтальный баннер: естественные пропорции, без object-cover */}
              <img
                src={HERO_ASIDE_BANNER}
                alt="ComeBack — дополненная реальность в городах Узбекистана"
                width={1200}
                height={675}
                className="h-auto w-full align-middle"
                decoding="async"
                fetchPriority="high"
              />
              <figcaption className="border-t border-slate-800/90 bg-slate-950/95 px-4 py-3 text-center text-xs text-slate-400">
                AR в Бухаре, Самарканде, Хиве и других городах
              </figcaption>
            </figure>
          </div>
        </div>
      </section>

      {/* Вертикальный постер: полная ширина, без обрезки текста сверху */}
      <section className="border-b border-slate-800/70 bg-gradient-to-b from-slate-950 via-slate-900/95 to-slate-950 py-10 md:py-16">
        <div className="container-page">
          <p className="mb-6 text-center text-sm font-medium tracking-wide text-emerald-400/95">
            Визуал приложения — постер и магазины приложений
          </p>
          <div className="mx-auto flex max-w-6xl justify-center rounded-2xl border border-slate-800/80 bg-slate-950/90 p-4 shadow-inner ring-1 ring-white/5 sm:p-6 md:p-8">
            <img
              src={POSTER_MAIN}
              alt="Augmented Reality in the Cities of Uzbekistan — ComeBack"
              width={1080}
              height={1920}
              className="h-auto max-h-[min(88vh,960px)] w-full max-w-3xl object-contain object-top"
              decoding="async"
            />
          </div>
        </div>
      </section>

      <section className="border-b border-slate-800/70 bg-slate-950 py-10 md:py-14">
        <div className="container-page space-y-6">
          <h2 className="text-center text-lg font-semibold text-slate-50 md:text-xl">
            ComeBack в деталях
          </h2>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {detailTiles.map((b) => (
              <figure
                key={b.src}
                className="flex flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/50 shadow-lg ring-1 ring-white/5"
              >
                <div className="flex min-h-[12rem] flex-1 items-center justify-center bg-slate-950/60 p-3 sm:min-h-[14rem] sm:p-4">
                  <img
                    src={b.src}
                    alt={b.alt}
                    width={800}
                    height={450}
                    className="max-h-56 w-full object-contain sm:max-h-64"
                    loading="lazy"
                    decoding="async"
                  />
                </div>
              </figure>
            ))}
          </div>
        </div>
      </section>

      <section className="border-b border-slate-800/70 bg-slate-900/30 py-10 md:py-14">
        <div className="container-page">
          <h2 className="mb-2 text-center text-lg font-semibold text-slate-50 md:text-xl">
            Галерея сцен AR
          </h2>
          <p className="mx-auto mb-8 max-w-2xl text-center text-sm text-slate-400">
            Слайды разного формата показываются целиком (без обрезки). Листайте,
            чтобы увидеть локации в Узбекистане.
          </p>
          <div className="relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 shadow-xl ring-1 ring-white/5">
            <div className="flex min-h-[min(70vh,640px)] items-center justify-center bg-[radial-gradient(ellipse_at_center,_#0f172a_0%,_#020617_70%)] px-3 py-8 sm:min-h-[min(75vh,720px)] sm:px-6 sm:py-10">
              <img
                key={gallerySlides[slideIndex]}
                src={gallerySlides[slideIndex]}
                alt={`Слайд ${slideIndex + 1} — ComeBack AR`}
                width={1200}
                height={1200}
                className="max-h-[min(68vh,700px)] w-full object-contain"
                decoding="async"
              />
            </div>
            <div className="flex items-center justify-between gap-2 border-t border-slate-800 bg-slate-900/90 px-3 py-3 sm:px-4">
              <button
                type="button"
                onClick={prevSlide}
                className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 hover:border-emerald-500/50 hover:text-emerald-300"
                aria-label="Предыдущий слайд"
              >
                ←
              </button>
              <div className="flex flex-wrap justify-center gap-1.5">
                {gallerySlides.map((_, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => setSlideIndex(i)}
                    className={`h-2 w-2 rounded-full transition-colors ${
                      i === slideIndex
                        ? "bg-emerald-400"
                        : "bg-slate-600 hover:bg-slate-500"
                    }`}
                    aria-label={`Слайд ${i + 1}`}
                  />
                ))}
              </div>
              <button
                type="button"
                onClick={nextSlide}
                className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 hover:border-emerald-500/50 hover:text-emerald-300"
                aria-label="Следующий слайд"
              >
                →
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="border-b border-slate-800/70 bg-slate-950">
        <div className="container-page grid gap-10 py-12 md:grid-cols-[3fr,2fr] md:py-16">
          <div className="space-y-5">
            <h2 className="text-xl font-semibold tracking-tight text-slate-50 md:text-2xl">
              Что вы получите с ComeBack
            </h2>
            <div className="grid gap-4 md:grid-cols-3">
              {features.map((feature) => (
                <div
                  key={feature.title}
                  className="space-y-2 rounded-2xl border border-slate-800 bg-slate-900/40 p-4"
                >
                  <h3 className="text-sm font-semibold text-slate-50">
                    {feature.title}
                  </h3>
                  <p className="text-xs text-slate-300">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
          <div className="space-y-4 rounded-2xl border border-slate-800 bg-slate-900/40 p-5">
            <h2
              id="download"
              className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-400"
            >
              КАК НАЧАТЬ
            </h2>
            <ol className="space-y-3 text-sm text-slate-200">
              {steps.map((step, index) => (
                <li key={step} className="flex gap-3">
                  <span className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500/10 text-xs font-semibold text-emerald-400 ring-1 ring-emerald-500/40">
                    {index + 1}
                  </span>
                  <p>{step}</p>
                </li>
              ))}
            </ol>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <a
                href="https://apps.apple.com/app/id0000000000"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-3 rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-2 text-left text-xs text-slate-100 hover:border-emerald-500 hover:bg-slate-900 transition-colors"
              >
                <div className="flex h-7 w-7 items-center justify-center rounded-xl bg-slate-800">
                  <span className="text-[10px] font-semibold"></span>
                </div>
                <div className="leading-tight">
                  <div className="text-[10px] uppercase tracking-[0.18em] text-slate-400">
                    Скачать в
                  </div>
                  <div className="text-sm font-semibold">App Store</div>
                </div>
              </a>
              <a
                href="https://play.google.com/store/apps/details?id=com.comeback.app"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-3 rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-2 text-left text-xs text-slate-100 hover:border-emerald-500 hover:bg-slate-900 transition-colors"
              >
                <div className="flex h-7 w-7 items-center justify-center rounded-xl bg-slate-800">
                  <span className="text-[10px] font-semibold">▶</span>
                </div>
                <div className="leading-tight">
                  <div className="text-[10px] uppercase tracking-[0.18em] text-slate-400">
                    Доступно в
                  </div>
                  <div className="text-sm font-semibold">Google Play</div>
                </div>
              </a>
            </div>
            <p className="pt-3 text-xs text-slate-400">
              Приложение развивается — мы добавляем новые города, маршруты и
              исторические сценарии, чтобы вы могли по‑новому увидеть знакомые
              места.
            </p>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-800/70 bg-slate-950/95">
        <div className="container-page flex flex-col gap-3 py-5 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <span>© {new Date().getFullYear()} ComeBack. Все права защищены.</span>
          <div className="flex flex-wrap items-center gap-3">
            <a
              href="mailto:hello@comeback.uz"
              className="text-slate-400 underline-offset-2 hover:text-emerald-300 hover:underline"
            >
              Связаться с нами
            </a>
            <span className="hidden h-1 w-1 rounded-full bg-slate-700 sm:inline-block" />
            <a
              href="/offer"
              className="text-slate-400 underline-offset-2 hover:text-emerald-300 hover:underline"
            >
              Публичная оферта
            </a>
            <span className="hidden h-1 w-1 rounded-full bg-slate-700 sm:inline-block" />
            <a
              href="/privacy"
              className="text-slate-400 underline-offset-2 hover:text-emerald-300 hover:underline"
            >
              Политика конфиденциальности
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

