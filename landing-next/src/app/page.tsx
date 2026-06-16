"use client";

import Image from "next/image";
import { useState } from "react";

const heroBanners = [
  {
    src: "/images/landing/6.png",
    label: "Слайд 1",
    alt: "ComeBack баннер 1",
  },
  {
    src: "/images/landing/7.png",
    label: "Слайд 2",
    alt: "ComeBack баннер 2",
  },
  {
    src: "/images/landing/8.png",
    label: "Слайд 3",
    alt: "ComeBack баннер 3",
  },
] as const;

const features = [
  {
    icon: "🏛️",
    title: "Бухара времён караванов",
    description:
      "Узкие улицы, медресе и базары — как в эпоху Великого Шёлкового пути.",
  },
  {
    icon: "✨",
    title: "Самарканд и его легенды",
    description:
      "Площади и мавзолеи в масштабе, который сложно представить только по учебникам.",
  },
  {
    icon: "🕌",
    title: "Хива и другие локации",
    description:
      "Крепости и кварталы: добавляются новые маршруты и сценарии.",
  },
];

const steps = [
  "Скачайте ComeBack в App Store или Google Play.",
  "Выберите город и точку на карте рядом с собой.",
  "Наведите камеру — на экране появится слой прошлого поверх настоящего.",
];

const cities = ["Бухара", "Самарканд", "Хива", "Ташкент", "Шахрисабз"];

export default function LandingPage() {
  const [heroIndex, setHeroIndex] = useState(0);

  const nextHero = () =>
    setHeroIndex((i) => (i + 1) % heroBanners.length);
  const prevHero = () =>
    setHeroIndex((i) => (i - 1 + heroBanners.length) % heroBanners.length);

  return (
    <div className="landing-bg flex min-h-screen flex-col">
      <header className="glass-header">
        <div className="container-page flex min-h-16 flex-wrap items-center justify-between gap-y-3 py-3 sm:h-[4.25rem] sm:py-0">
          <a href="/" className="flex shrink-0 items-center gap-2.5 sm:gap-3">
            <Image
              src="/images/landing/CRAFT%20SHOP.png"
              alt="Come Back AR"
              width={336}
              height={84}
              className="h-8 w-auto sm:h-10"
              priority
            />
          </a>

          <nav className="flex w-full flex-wrap items-center justify-center gap-x-4 gap-y-2 text-[11px] font-medium text-slate-300 sm:w-auto sm:justify-end sm:gap-x-6 sm:text-sm md:gap-x-8">
            <a href="#hero" className="transition hover:text-white">
              Главная
            </a>
            <a href="#cities" className="transition hover:text-white">
              Города
            </a>
            <a
              href="#download"
              className="rounded-full bg-white/10 px-3 py-1.5 text-white ring-1 ring-white/15 transition hover:bg-emerald-500/20 hover:ring-emerald-400/40 sm:px-4 sm:py-2"
            >
              Скачать
            </a>
          </nav>
        </div>
      </header>

      {/* Hero: основной слайдер с 3 баннерами */}
      <section
        id="hero"
        className="relative overflow-hidden border-b border-white/5 pb-10 pt-6 sm:pb-14 sm:pt-8 md:pt-10"
      >
        <div className="pointer-events-none absolute -right-32 top-10 h-64 w-64 rounded-full bg-emerald-500/10 blur-[100px] sm:h-80 sm:w-80" />
        <div className="pointer-events-none absolute -left-24 top-40 h-56 w-56 rounded-full bg-teal-500/10 blur-[90px]" />

        <div className="container-page">
          <p className="mb-3 text-center text-[10px] font-semibold uppercase tracking-[0.2em] text-emerald-400/90 sm:mb-4 sm:text-[11px]">
            Исторические персонажи · локации приложения
          </p>

          <div className="relative mx-auto max-w-6xl overflow-hidden rounded-2xl border border-white/10 bg-black shadow-2xl ring-1 ring-white/10 sm:rounded-3xl">
            <div className="relative flex min-h-[min(42vh,320px)] items-center justify-center bg-gradient-to-b from-slate-950 to-black px-2 py-6 sm:min-h-[min(50vh,400px)] sm:px-4 sm:py-8 md:min-h-[min(56vh,480px)] lg:min-h-[min(60vh,520px)]">
              <img
                key={heroBanners[heroIndex].src}
                src={heroBanners[heroIndex].src}
                alt={heroBanners[heroIndex].alt}
                width={1920}
                height={720}
                className="h-auto w-full max-h-[min(38vh,300px)] object-contain object-center sm:max-h-[min(46vh,380px)] md:max-h-[min(52vh,440px)] lg:max-h-[min(56vh,500px)]"
                decoding="async"
                fetchPriority="high"
              />
            </div>
            <div className="border-t border-white/10 bg-slate-950/95 px-3 py-3 sm:px-5 sm:py-4">
              <p className="mb-3 text-center text-[11px] font-medium text-slate-400 sm:mb-3 sm:text-xs">
                Баннер{" "}
                <span className="text-emerald-400">{heroBanners[heroIndex].label}</span>
                {" · "}
                {heroIndex + 1} / {heroBanners.length}
              </p>
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between sm:gap-4">
                <button
                  type="button"
                  onClick={prevHero}
                  className="order-2 min-h-[44px] rounded-xl border border-slate-600 bg-slate-800/90 px-4 py-2.5 text-sm font-medium text-white transition hover:border-emerald-500/50 sm:order-1 sm:min-h-0 sm:px-5"
                  aria-label="Предыдущий баннер"
                >
                  ← Назад
                </button>
                <div className="order-1 flex flex-wrap justify-center gap-2 sm:order-2">
                  {heroBanners.map((b, i) => (
                    <button
                      key={b.src}
                      type="button"
                      onClick={() => setHeroIndex(i)}
                      className={`min-h-[44px] min-w-[44px] rounded-full text-[10px] font-semibold uppercase tracking-wider transition sm:min-h-0 sm:min-w-0 sm:px-3 sm:py-1.5 sm:text-[11px] ${
                        i === heroIndex
                          ? "bg-emerald-500 text-slate-950 ring-2 ring-emerald-300/50"
                          : "bg-slate-800 text-slate-400 ring-1 ring-white/10 hover:bg-slate-700 hover:text-white"
                      }`}
                      aria-label={`Баннер: ${b.label}`}
                    >
                      <span className="px-2 sm:px-0">{b.label}</span>
                    </button>
                  ))}
                </div>
                <button
                  type="button"
                  onClick={nextHero}
                  className="order-3 min-h-[44px] rounded-xl border border-slate-600 bg-slate-800/90 px-4 py-2.5 text-sm font-medium text-white transition hover:border-emerald-500/50 sm:min-h-0 sm:px-5"
                  aria-label="Следующий баннер"
                >
                  Вперёд →
                </button>
              </div>
            </div>
          </div>

          <div className="mx-auto mt-8 max-w-3xl space-y-6 text-center sm:mt-10 sm:space-y-8">
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-500/[0.07] px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-emerald-300/95 sm:px-4 sm:text-[11px]">
              <span className="relative flex h-2 w-2 shrink-0">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
              </span>
              COMEBACK.UZ
            </div>

            <h1 className="text-balance text-3xl font-bold leading-[1.12] tracking-tight text-white sm:text-4xl md:text-5xl">
              Увидьте{" "}
              <span className="bg-gradient-to-r from-emerald-300 via-teal-200 to-cyan-300 bg-clip-text text-transparent">
                Бухару, Самарканд и Хиву
              </span>{" "}
              такими, какими они были раньше
            </h1>

            <p className="mx-auto max-w-xl text-pretty text-sm leading-relaxed text-slate-400 sm:text-base md:text-lg">
              На исторической площади откройте камеру — поверх сегодняшнего
              города появятся реконструкции улиц, стен и жизни прошлых эпох.
            </p>

            <div className="flex flex-col items-stretch gap-3 min-[420px]:flex-row min-[420px]:flex-wrap min-[420px]:justify-center">
              <a href="#download" className="btn-primary px-6 py-3 text-center text-sm sm:px-8 sm:text-base">
                Скачать приложение
              </a>
              <a href="#cities" className="btn-outline px-6 py-3 text-center text-sm sm:px-8 sm:text-base">
                Города и локации
              </a>
            </div>

            <div
              id="cities"
              className="mx-auto grid max-w-xl grid-cols-1 gap-2 min-[400px]:grid-cols-3 sm:gap-3"
            >
              {[
                { k: "Города", v: "в одном приложении" },
                { k: "AR", v: "на месте в реальном времени" },
                { k: "История", v: "через камеру телефона" },
              ].map((s) => (
                <div key={s.k} className="stat-pill py-2.5 sm:py-3">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-400/90 sm:text-xs">
                    {s.k}
                  </div>
                  <div className="mt-0.5 text-[11px] leading-snug text-slate-300 sm:text-xs">
                    {s.v}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="container-page mt-8 sm:mt-10">
          <div className="flex flex-wrap justify-center gap-2 sm:gap-2.5">
            {cities.map((city) => (
              <span
                key={city}
                className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-[11px] font-medium text-slate-300 sm:px-4 sm:py-2 sm:text-sm"
              >
                {city}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Возможности + скачать */}
      <section className="py-12 sm:py-16 md:py-20">
        <div className="container-page grid gap-10 lg:grid-cols-12 lg:gap-14 xl:gap-16">
          <div className="space-y-6 lg:col-span-7 lg:space-y-8">
            <div>
              <p className="section-eyebrow mb-2 sm:mb-3">Возможности</p>
              <h2 className="text-xl font-bold text-white sm:text-2xl md:text-3xl lg:text-4xl">
                Что вы получите с ComeBack
              </h2>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-3">
              {features.map((f) => (
                <div key={f.title} className="feature-card !p-5 sm:!p-6">
                  <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-500/15 text-xl ring-1 ring-emerald-500/25 sm:mb-4 sm:h-12 sm:w-12 sm:text-2xl">
                    {f.icon}
                  </div>
                  <h3 className="text-sm font-semibold text-white sm:text-base">{f.title}</h3>
                  <p className="mt-2 text-xs leading-relaxed text-slate-400 sm:text-sm">
                    {f.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div
            id="download"
            className="lg:col-span-5 lg:sticky lg:top-20 lg:self-start"
          >
            <div className="rounded-2xl border border-emerald-500/20 bg-gradient-to-b from-emerald-950/40 to-slate-950/90 p-5 shadow-xl shadow-emerald-900/20 ring-1 ring-emerald-500/10 sm:rounded-3xl sm:p-7 md:p-8">
              <p className="section-eyebrow mb-1.5 text-emerald-300">Старт</p>
              <h3 className="text-lg font-bold text-white sm:text-xl md:text-2xl">
                Три шага до AR
              </h3>
              <ol className="mt-5 space-y-3 sm:mt-6 sm:space-y-4">
                {steps.map((step, index) => (
                  <li key={step} className="flex gap-3 sm:gap-4">
                    <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-emerald-500/20 text-xs font-bold text-emerald-300 ring-1 ring-emerald-400/30 sm:h-9 sm:w-9 sm:text-sm">
                      {index + 1}
                    </span>
                    <p className="text-xs leading-relaxed text-slate-300 sm:text-sm md:text-base">
                      {step}
                    </p>
                  </li>
                ))}
              </ol>

              <div className="mt-6 flex flex-col gap-2.5 sm:mt-8 sm:gap-3">
                <a
                  href="https://apps.apple.com/app/id0000000000"
                  target="_blank"
                  rel="noreferrer"
                  className="flex min-h-[52px] items-center gap-3 rounded-2xl border border-white/10 bg-black/30 px-4 py-3 transition hover:border-emerald-400/40 sm:gap-4 sm:px-5 sm:py-4"
                >
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-base font-semibold text-black">
                    
                  </span>
                  <div className="min-w-0">
                    <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-500">
                      Загрузить в
                    </div>
                    <div className="truncate text-base font-bold text-white sm:text-lg">
                      App Store
                    </div>
                  </div>
                </a>
                <a
                  href="https://play.google.com/store/apps/details?id=com.comeback.app"
                  target="_blank"
                  rel="noreferrer"
                  className="flex min-h-[52px] items-center gap-3 rounded-2xl border border-white/10 bg-black/30 px-4 py-3 transition hover:border-emerald-400/40 sm:gap-4 sm:px-5 sm:py-4"
                >
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-500 text-sm font-bold text-slate-950">
                    ▶
                  </span>
                  <div className="min-w-0">
                    <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-500">
                      Доступно в
                    </div>
                    <div className="truncate text-base font-bold text-white sm:text-lg">
                      Google Play
                    </div>
                  </div>
                </a>
              </div>

              <p className="mt-5 border-t border-white/10 pt-5 text-[11px] leading-relaxed text-slate-500 sm:mt-6 sm:pt-6 sm:text-xs">
                Добавляем города и сценарии — следите за обновлениями в магазине.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="border-t border-emerald-500/20 bg-gradient-to-r from-emerald-600/90 via-teal-600/85 to-cyan-700/90 py-10 sm:py-14 md:py-16">
        <div className="container-page flex flex-col items-stretch gap-6 text-center md:flex-row md:items-center md:justify-between md:text-left">
          <div className="max-w-xl md:pr-6">
            <h2 className="text-xl font-bold text-white sm:text-2xl md:text-3xl">
              Готовы увидеть древний Узбекистан в AR?
            </h2>
            <p className="mt-2 text-sm text-emerald-50/90 sm:text-base">
              Установите ComeBack и откройте камеру на исторической площади.
            </p>
          </div>
          <div className="flex w-full shrink-0 flex-col gap-3 sm:max-w-md sm:flex-row md:w-auto md:flex-col lg:flex-row">
            <a
              href="#download"
              className="inline-flex min-h-[48px] items-center justify-center rounded-full bg-slate-950 px-6 py-3 text-sm font-bold text-white shadow-xl transition hover:bg-slate-900 sm:px-8"
            >
              К загрузке
            </a>
            <a
              href="mailto:hello@comeback.uz"
              className="inline-flex min-h-[48px] items-center justify-center rounded-full border-2 border-white/40 bg-white/10 px-6 py-3 text-sm font-semibold text-white backdrop-blur-sm transition hover:bg-white/20 sm:px-8"
            >
              hello@comeback.uz
            </a>
          </div>
        </div>
      </section>

      <footer className="border-t border-white/5 bg-[#020617] py-8 sm:py-10 md:py-12">
        <div className="container-page grid gap-8 sm:grid-cols-2 sm:gap-10 lg:grid-cols-4">
          <div className="sm:col-span-2 lg:col-span-2">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-600 text-base font-bold text-slate-950 sm:h-10 sm:w-10 sm:text-lg">
                C
              </div>
              <span className="text-base font-bold text-white sm:text-lg">ComeBack</span>
            </div>
            <p className="mt-3 max-w-sm text-xs leading-relaxed text-slate-500 sm:mt-4 sm:text-sm">
              Проект LEMALA MChJ. AR для туристов и жителей: Бухара, Самарканд,
              Хива и другие локации.
            </p>
          </div>
          <div>
            <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 sm:text-xs">
              Навигация
            </div>
            <ul className="mt-3 space-y-1.5 text-xs text-slate-400 sm:mt-4 sm:space-y-2 sm:text-sm">
              <li>
                <a href="#hero" className="hover:text-emerald-400">
                  Главная
                </a>
              </li>
              <li>
                <a href="#cities" className="hover:text-emerald-400">
                  Города
                </a>
              </li>
              <li>
                <a href="#download" className="hover:text-emerald-400">
                  Скачать
                </a>
              </li>
            </ul>
          </div>
          <div>
            <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 sm:text-xs">
              Документы
            </div>
            <ul className="mt-3 space-y-1.5 text-xs text-slate-400 sm:mt-4 sm:space-y-2 sm:text-sm">
              <li>
                <a href="/offer" className="hover:text-emerald-400">
                  Публичная оферта
                </a>
              </li>
              <li>
                <a href="/privacy" className="hover:text-emerald-400">
                  Конфиденциальность
                </a>
              </li>
              <li>
                <a href="mailto:hello@comeback.uz" className="hover:text-emerald-400">
                  hello@comeback.uz
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="container-page mt-8 border-t border-white/5 pt-5 text-center text-[10px] text-slate-600 sm:mt-10 sm:pt-6 sm:text-left sm:text-xs">
          © {new Date().getFullYear()} ComeBack · LEMALA MChJ
        </div>
      </footer>
    </div>
  );
}
