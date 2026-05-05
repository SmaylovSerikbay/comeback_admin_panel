"use client";

import { useState } from "react";

const HERO_ASIDE_BANNER = "/images/landing/banner1.png";
const POSTER_MAIN = "/images/landing/slideshow1_ru.png";

const detailTiles = [
  {
    src: "/images/landing/banner2.png",
    alt: "ComeBack — исторические города Узбекистана в AR",
    title: "Города Шёлкового пути",
    caption: "Бухара, Самарканд, Хива — в одном приложении",
  },
  {
    src: "/images/landing/banner3.png",
    alt: "ComeBack — путешествие во времени",
    title: "Путешествие во времени",
    caption: "Сравнивайте «тогда» и «сейчас» на одной площади",
  },
  {
    src: "/images/landing/slideshow2.png",
    alt: "Дополненная реальность в городах Узбекистана",
    title: "AR на исторических площадях",
    caption: "Навёл камеру — увидел реконструкцию прошлого",
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
    icon: "🏛️",
    title: "Бухара времён караванов",
    description:
      "Узкие улицы, медресе и базары — как в эпоху Великого Шёлкового пути. Прогулка по живой истории.",
  },
  {
    icon: "✨",
    title: "Самарканд и его легенды",
    description:
      "Площади и мавзолеи в масштабе, который сложно представить только по учебникам — увидите в AR.",
  },
  {
    icon: "🕌",
    title: "Хива и другие локации",
    description:
      "Крепости, минареты и кварталы: приложение развивается, добавляются новые маршруты и сценарии.",
  },
];

const steps = [
  "Скачайте ComeBack в App Store или Google Play.",
  "Выберите город и точку на карте рядом с собой.",
  "Наведите камеру — на экране появится слой прошлого поверх настоящего.",
];

const cities = ["Бухара", "Самарканд", "Хива", "Ташкент", "Шахрисабз"];

export default function LandingPage() {
  const [slideIndex, setSlideIndex] = useState(0);
  const nextSlide = () =>
    setSlideIndex((i) => (i + 1) % gallerySlides.length);
  const prevSlide = () =>
    setSlideIndex((i) => (i - 1 + gallerySlides.length) % gallerySlides.length);

  return (
    <div className="landing-bg flex min-h-screen flex-col">
      <header className="glass-header">
        <div className="container-page flex h-16 items-center justify-between gap-4 sm:h-[4.25rem]">
          <a href="#" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-600 text-lg font-bold text-slate-950 shadow-lg shadow-emerald-500/30">
              C
            </div>
            <div>
              <div className="text-sm font-bold tracking-tight text-white sm:text-base">
                ComeBack
              </div>
              <div className="text-[11px] text-slate-400 sm:text-xs">
                AR по древним городам Узбекистана
              </div>
            </div>
          </a>

          <nav className="hidden items-center gap-8 text-sm font-medium text-slate-300 md:flex">
            <a href="#cities" className="transition hover:text-white">
              Города
            </a>
            <a href="#visual" className="transition hover:text-white">
              Визуал
            </a>
            <a href="#gallery" className="transition hover:text-white">
              Галерея
            </a>
            <a
              href="#download"
              className="rounded-full bg-white/10 px-4 py-2 text-white ring-1 ring-white/15 transition hover:bg-emerald-500/20 hover:ring-emerald-400/40"
            >
              Скачать
            </a>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-white/5 pb-16 pt-10 sm:pb-20 sm:pt-14 md:pt-16">
        <div className="pointer-events-none absolute -right-32 top-20 h-96 w-96 rounded-full bg-emerald-500/15 blur-[100px]" />
        <div className="pointer-events-none absolute -left-40 bottom-0 h-80 w-80 rounded-full bg-teal-500/10 blur-[90px]" />

        <div className="container-page relative grid gap-12 lg:grid-cols-12 lg:gap-10 lg:items-center">
          <div className="space-y-8 lg:col-span-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-500/[0.07] px-4 py-1.5 text-[11px] font-semibold uppercase tracking-[0.2em] text-emerald-300/95">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
              </span>
              COMEBACK.UZ · AR в Узбекистане
            </div>

            <h1 className="text-balance text-4xl font-bold leading-[1.1] tracking-tight text-white sm:text-5xl md:text-6xl lg:text-[3.25rem] xl:text-6xl">
              Увидьте{" "}
              <span className="bg-gradient-to-r from-emerald-300 via-teal-200 to-cyan-300 bg-clip-text text-transparent">
                Бухару, Самарканд и Хиву
              </span>{" "}
              такими, какими они были раньше
            </h1>

            <p className="max-w-xl text-pretty text-base leading-relaxed text-slate-400 sm:text-lg">
              Мобильное приложение дополненной реальности: на исторической
              площади откройте камеру — и поверх сегодняшнего города появятся
              реконструкции улиц, стен и жизни прошлых эпох.
            </p>

            <div className="flex flex-col gap-4 sm:flex-row sm:flex-wrap sm:items-center">
              <a href="#download" className="btn-primary px-8 py-3.5 text-base">
                Скачать приложение
              </a>
              <a href="#gallery" className="btn-outline px-8 py-3.5 text-base">
                Смотреть галерею
              </a>
            </div>

            <div
              id="cities"
              className="grid grid-cols-3 gap-3 pt-2 sm:max-w-lg sm:gap-4"
            >
              {[
                { k: "Города", v: "в одном приложении" },
                { k: "AR", v: "на месте, в реальном времени" },
                { k: "История", v: "через камеру телефона" },
              ].map((s) => (
                <div key={s.k} className="stat-pill">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-400/90 sm:text-xs">
                    {s.k}
                  </div>
                  <div className="mt-1 text-[11px] leading-snug text-slate-300 sm:text-xs">
                    {s.v}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="relative lg:col-span-6">
            <div className="absolute -inset-1 rounded-3xl bg-gradient-to-br from-emerald-500/20 via-transparent to-teal-500/20 opacity-70 blur-xl" />
            <figure className="relative overflow-hidden rounded-3xl border border-white/10 bg-slate-900/80 shadow-2xl ring-1 ring-white/10">
              <img
                src={HERO_ASIDE_BANNER}
                alt="ComeBack — дополненная реальность в городах Узбекистана"
                width={1200}
                height={675}
                className="h-auto w-full align-middle"
                decoding="async"
                fetchPriority="high"
              />
              <figcaption className="flex flex-wrap items-center justify-between gap-2 border-t border-white/10 bg-slate-950/90 px-4 py-3 text-xs text-slate-400">
                <span>Официальный визуал проекта</span>
                <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 font-medium text-emerald-300">
                  Бухара · Самарканд · Хива
                </span>
              </figcaption>
            </figure>
          </div>
        </div>

        {/* Лента городов */}
        <div className="container-page mt-14 sm:mt-16">
          <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-3">
            {cities.map((city) => (
              <span
                key={city}
                className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs font-medium text-slate-300 sm:text-sm"
              >
                {city}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Постер приложения */}
      <section
        id="visual"
        className="border-b border-white/5 bg-gradient-to-b from-slate-950/80 to-[#030712] py-14 sm:py-20"
      >
        <div className="container-page">
          <div className="mx-auto mb-10 max-w-2xl text-center">
            <p className="section-eyebrow mb-3">Визуал приложения</p>
            <h2 className="text-2xl font-bold text-white sm:text-3xl md:text-4xl">
              Постер и магазины приложений — как выглядит ComeBack
            </h2>
            <p className="mt-4 text-sm leading-relaxed text-slate-400 sm:text-base">
              Ниже — макет в высоком разрешении: весь текст и кнопки магазинов
              видны целиком, без обрезки.
            </p>
          </div>

          <div className="mx-auto max-w-4xl rounded-3xl border border-white/10 bg-gradient-to-b from-slate-900/60 to-slate-950/90 p-3 shadow-[0_0_0_1px_rgba(255,255,255,0.06)_inset] sm:p-5 md:p-8">
            <div className="overflow-hidden rounded-2xl ring-1 ring-black/40">
              <img
                src={POSTER_MAIN}
                alt="Augmented Reality in the Cities of Uzbekistan — ComeBack"
                width={1080}
                height={1920}
                className="mx-auto h-auto max-h-[min(85vh,920px)] w-full object-contain object-top"
                decoding="async"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Три карточки с картинками */}
      <section className="border-b border-white/5 py-14 sm:py-16">
        <div className="container-page">
          <div className="mb-10 flex flex-col gap-4 text-center sm:mb-14">
            <p className="section-eyebrow">Материалы проекта</p>
            <h2 className="text-2xl font-bold text-white sm:text-3xl">
              Ключевые кадры и смыслы
            </h2>
            <p className="mx-auto max-w-2xl text-sm text-slate-400 sm:text-base">
              Три разных визуала: маршруты, атмосфера путешествия во времени и
              сцены AR на узбекских площадях.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3 md:gap-8">
            {detailTiles.map((b) => (
              <article
                key={b.src}
                className="feature-card flex flex-col"
              >
                <div className="relative mb-4 flex min-h-[200px] flex-1 items-center justify-center rounded-xl bg-[#0a0f1a] p-4 ring-1 ring-white/5 sm:min-h-[220px]">
                  <img
                    src={b.src}
                    alt={b.alt}
                    width={800}
                    height={450}
                    className="max-h-52 w-full object-contain sm:max-h-56"
                    loading="lazy"
                    decoding="async"
                  />
                </div>
                <h3 className="text-lg font-semibold text-white">{b.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {b.caption}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Галерея */}
      <section
        id="gallery"
        className="border-b border-white/5 bg-slate-950/50 py-14 sm:py-20"
      >
        <div className="container-page">
          <div className="mx-auto mb-10 max-w-2xl text-center sm:mb-12">
            <p className="section-eyebrow mb-3">Галерея</p>
            <h2 className="text-2xl font-bold text-white sm:text-3xl md:text-4xl">
              Сцены AR в городах Узбекистана
            </h2>
            <p className="mt-4 text-sm text-slate-400 sm:text-base">
              Листайте слайды — каждый показан полностью, в удобном для экрана
              масштабе.
            </p>
          </div>

          <div className="mx-auto max-w-5xl overflow-hidden rounded-3xl border border-white/10 bg-[#070d18] shadow-2xl ring-1 ring-white/5">
            <div className="relative flex min-h-[min(62vh,560px)] items-center justify-center bg-[radial-gradient(ellipse_80%_60%_at_50%_40%,#0f172a_0%,#020617_75%)] px-4 py-10 sm:min-h-[min(68vh,640px)] sm:px-8 sm:py-12">
              <img
                key={gallerySlides[slideIndex]}
                src={gallerySlides[slideIndex]}
                alt={`Слайд ${slideIndex + 1} — ComeBack AR`}
                width={1200}
                height={1200}
                className="max-h-[min(60vh,620px)] w-full object-contain drop-shadow-2xl transition-opacity duration-300"
                decoding="async"
              />
            </div>
            <div className="flex flex-col gap-4 border-t border-white/10 bg-slate-950/95 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
              <button
                type="button"
                onClick={prevSlide}
                className="order-2 rounded-xl border border-slate-600 bg-slate-800/80 px-5 py-2.5 text-sm font-medium text-white transition hover:border-emerald-500/50 hover:bg-slate-800 sm:order-1"
                aria-label="Предыдущий слайд"
              >
                ← Назад
              </button>
              <div className="order-1 flex justify-center gap-2 sm:order-2">
                {gallerySlides.map((_, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => setSlideIndex(i)}
                    className={`h-2.5 rounded-full transition-all ${
                      i === slideIndex
                        ? "w-8 bg-emerald-400"
                        : "w-2.5 bg-slate-600 hover:bg-slate-500"
                    }`}
                    aria-label={`Слайд ${i + 1}`}
                  />
                ))}
              </div>
              <button
                type="button"
                onClick={nextSlide}
                className="order-3 rounded-xl border border-slate-600 bg-slate-800/80 px-5 py-2.5 text-sm font-medium text-white transition hover:border-emerald-500/50 hover:bg-slate-800"
                aria-label="Следующий слайд"
              >
                Вперёд →
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Фичи + скачать */}
      <section className="py-14 sm:py-20">
        <div className="container-page grid gap-12 lg:grid-cols-12 lg:gap-16">
          <div className="space-y-8 lg:col-span-7">
            <div>
              <p className="section-eyebrow mb-3">Возможности</p>
              <h2 className="text-2xl font-bold text-white sm:text-3xl md:text-4xl">
                Что вы получите с ComeBack
              </h2>
            </div>
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-3">
              {features.map((f) => (
                <div key={f.title} className="feature-card !p-6">
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/15 text-2xl ring-1 ring-emerald-500/25">
                    {f.icon}
                  </div>
                  <h3 className="text-base font-semibold text-white">{f.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-slate-400">
                    {f.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div
            id="download"
            className="lg:col-span-5 lg:sticky lg:top-24 lg:self-start"
          >
            <div className="rounded-3xl border border-emerald-500/20 bg-gradient-to-b from-emerald-950/40 to-slate-950/90 p-6 shadow-xl shadow-emerald-900/20 ring-1 ring-emerald-500/10 sm:p-8">
              <p className="section-eyebrow mb-2 text-emerald-300">Старт</p>
              <h3 className="text-xl font-bold text-white sm:text-2xl">
                Как начать за три шага
              </h3>
              <ol className="mt-6 space-y-4">
                {steps.map((step, index) => (
                  <li key={step} className="flex gap-4">
                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-500/20 text-sm font-bold text-emerald-300 ring-1 ring-emerald-400/30">
                      {index + 1}
                    </span>
                    <p className="text-sm leading-relaxed text-slate-300 sm:text-base">
                      {step}
                    </p>
                  </li>
                ))}
              </ol>

              <div className="mt-8 flex flex-col gap-3">
                <a
                  href="https://apps.apple.com/app/id0000000000"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-4 rounded-2xl border border-white/10 bg-black/30 px-5 py-4 transition hover:border-emerald-400/40 hover:bg-black/40"
                >
                  <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-lg font-semibold text-black">
                    
                  </span>
                  <div>
                    <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-500">
                      Загрузить в
                    </div>
                    <div className="text-lg font-bold text-white">App Store</div>
                  </div>
                </a>
                <a
                  href="https://play.google.com/store/apps/details?id=com.comeback.app"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-4 rounded-2xl border border-white/10 bg-black/30 px-5 py-4 transition hover:border-emerald-400/40 hover:bg-black/40"
                >
                  <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-500 text-sm font-bold text-slate-950">
                    ▶
                  </span>
                  <div>
                    <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-500">
                      Доступно в
                    </div>
                    <div className="text-lg font-bold text-white">Google Play</div>
                  </div>
                </a>
              </div>

              <p className="mt-6 border-t border-white/10 pt-6 text-xs leading-relaxed text-slate-500">
                Мы регулярно добавляем города, маршруты и сценарии. Следите за
                обновлениями в магазине приложений.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Нижний CTA */}
      <section className="border-t border-emerald-500/20 bg-gradient-to-r from-emerald-600/90 via-teal-600/85 to-cyan-700/90 py-12 sm:py-16">
        <div className="container-page flex flex-col items-center gap-6 text-center md:flex-row md:justify-between md:text-left">
          <div className="max-w-xl">
            <h2 className="text-2xl font-bold text-white sm:text-3xl">
              Готовы увидеть древний Узбекистан в AR?
            </h2>
            <p className="mt-2 text-sm text-emerald-50/90 sm:text-base">
              Установите ComeBack и откройте камеру на исторической площади.
            </p>
          </div>
          <div className="flex shrink-0 flex-col gap-3 sm:flex-row">
            <a
              href="#download"
              className="inline-flex items-center justify-center rounded-full bg-slate-950 px-8 py-3.5 text-sm font-bold text-white shadow-xl transition hover:bg-slate-900"
            >
              К кнопкам загрузки
            </a>
            <a
              href="mailto:hello@comeback.uz"
              className="inline-flex items-center justify-center rounded-full border-2 border-white/40 bg-white/10 px-8 py-3.5 text-sm font-semibold text-white backdrop-blur-sm transition hover:bg-white/20"
            >
              hello@comeback.uz
            </a>
          </div>
        </div>
      </section>

      <footer className="border-t border-white/5 bg-[#020617] py-10 sm:py-12">
        <div className="container-page grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div className="lg:col-span-2">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-600 text-lg font-bold text-slate-950">
                C
              </div>
              <span className="text-lg font-bold text-white">ComeBack</span>
            </div>
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-slate-500">
              Проект LEMALA MChJ. Дополненная реальность для туристов и жителей,
              которые хотят увидеть Бухару, Самарканд и Хиву глазами прошлых
              эпох.
            </p>
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Навигация
            </div>
            <ul className="mt-4 space-y-2 text-sm text-slate-400">
              <li>
                <a href="#cities" className="hover:text-emerald-400">
                  Города
                </a>
              </li>
              <li>
                <a href="#visual" className="hover:text-emerald-400">
                  Визуал
                </a>
              </li>
              <li>
                <a href="#gallery" className="hover:text-emerald-400">
                  Галерея
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
            <div className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Документы
            </div>
            <ul className="mt-4 space-y-2 text-sm text-slate-400">
              <li>
                <a href="/offer" className="hover:text-emerald-400">
                  Публичная оферта
                </a>
              </li>
              <li>
                <a href="/privacy" className="hover:text-emerald-400">
                  Политика конфиденциальности
                </a>
              </li>
              <li>
                <a
                  href="mailto:hello@comeback.uz"
                  className="hover:text-emerald-400"
                >
                  hello@comeback.uz
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="container-page mt-10 border-t border-white/5 pt-6 text-center text-xs text-slate-600 sm:text-left">
          © {new Date().getFullYear()} ComeBack · LEMALA MChJ. Все права защищены.
        </div>
      </footer>
    </div>
  );
}
