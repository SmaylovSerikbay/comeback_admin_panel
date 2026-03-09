"use client";

const features = [
  {
    title: "Глубокая интеграция с Unity",
    description:
      "Стабильный backend и удобная админка для управления контентом AR-проектов без обновления приложения.",
  },
  {
    title: "Мощная аналитика",
    description:
      "Отслеживайте установки, оплаты, конверсии и сценарии использования в одном дашборде.",
  },
  {
    title: "Надёжная инфраструктура",
    description:
      "Django + PostgreSQL + Redis + Docker + SSL — продакшен-стек, готовый к высоким нагрузкам.",
  },
];

const steps = [
  "Оставьте заявку и опишите ваш кейс.",
  "Мы предложим архитектуру и запустим пилот.",
  "Подключим оплату, аналитику и поддержим релиз.",
];

export default function LandingPage() {
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
              <span className="text-sm font-semibold tracking-tight">
                ComeBack
              </span>
              <span className="text-xs text-slate-400">
                AR-платформа для бизнеса
              </span>
            </div>
          </div>

          <div className="hidden items-center gap-4 text-sm text-slate-300 md:flex">
            <span className="cursor-default text-xs uppercase tracking-[0.18em] text-emerald-400/80">
              AR / SUBSCRIPTION / ANALYTICS
            </span>
          </div>

          <a
            href="https://admin.comeback.uz"
            className="btn-outline text-xs md:text-sm"
          >
            Вход в админку
          </a>
        </div>
      </header>

      <section className="border-b border-slate-800/70 bg-[radial-gradient(circle_at_top,_#22c55e11,_transparent_55%),radial-gradient(circle_at_bottom,_#22c55e22,_transparent_55%)]">
        <div className="container-page flex flex-col gap-10 py-14 md:flex-row md:items-center md:py-20">
          <div className="flex-1 space-y-6">
            <p className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/5 px-3 py-1 text-xs font-medium uppercase tracking-[0.18em] text-emerald-300">
              LIVE PROJECT
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.8)]" />
              COMEBACK.UZ
            </p>
            <h1 className="text-balance text-3xl font-semibold tracking-tight text-slate-50 sm:text-4xl md:text-5xl">
              Платформа дополненной реальности,
              <span className="text-emerald-400"> которая умеет продавать</span>
            </h1>
            <p className="max-w-xl text-pretty text-sm text-slate-300 sm:text-base">
              Управляйте контентом, подписками и оплатами вашего AR-приложения
              через удобную веб‑панель. Без ручных обновлений, с готовой
              интеграцией под Unity и прозрачной аналитикой.
            </p>
            <div className="flex flex-wrap items-center gap-3">
              <a
                href="mailto:admin@comeback.uz?subject=ComeBack%20Landing%20Request"
                className="btn-primary"
              >
                Оставить заявку
              </a>
              <a
                href="https://admin.comeback.uz"
                className="btn-outline text-sm"
              >
                Смотреть админ‑панель
              </a>
              <span className="text-xs text-slate-400">
                Подходит для подписочных AR‑сервисов, игр и интерактивного
                маркетинга.
              </span>
            </div>
          </div>

          <div className="flex-1">
            <div className="relative mx-auto max-w-md rounded-3xl border border-emerald-500/40 bg-gradient-to-br from-slate-900/80 via-slate-900/40 to-slate-950/80 p-5 shadow-[0_0_80px_rgba(16,185,129,0.25)] backdrop-blur">
              <div className="mb-4 flex items-center justify-between text-xs text-slate-400">
                <span className="inline-flex items-center gap-1">
                  <span className="h-2 w-2 rounded-full bg-emerald-400" />
                  Реальные метрики
                </span>
                <span className="rounded-full bg-slate-900/80 px-2 py-0.5 text-[10px] uppercase tracking-[0.18em] text-slate-400">
                  DASHBOARD
                </span>
              </div>
              <div className="space-y-4 text-xs text-slate-200">
                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-3">
                    <p className="text-[11px] text-slate-400">
                      Активные подписки
                    </p>
                    <p className="mt-1 text-2xl font-semibold text-emerald-400">
                      12 480
                    </p>
                    <p className="mt-1 text-[11px] text-emerald-300">
                      +8.4% за 30 дней
                    </p>
                  </div>
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-3">
                    <p className="text-[11px] text-slate-400">
                      Месячный оборот
                    </p>
                    <p className="mt-1 text-2xl font-semibold text-slate-50">
                      74 200 $
                    </p>
                    <p className="mt-1 text-[11px] text-emerald-300">
                      конверсия в оплату 6.3%
                    </p>
                  </div>
                </div>
                <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-3">
                  <p className="text-[11px] text-slate-400 mb-2">
                    Пайплайн Unity → Backend → Клиент
                  </p>
                  <ol className="space-y-1 text-[11px] text-slate-300">
                    <li>• Unity отправляет события и покупки на backend.</li>
                    <li>• Django обрабатывает оплату и подписку.</li>
                    <li>• Firebase синхронизирует данные с приложением.</li>
                    <li>• Дашборд показывает, что происходит прямо сейчас.</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="border-b border-slate-800/70 bg-slate-950">
        <div className="container-page grid gap-10 py-12 md:grid-cols-[3fr,2fr] md:py-16">
          <div className="space-y-5">
            <h2 className="text-xl font-semibold tracking-tight text-slate-50 md:text-2xl">
              Что даёт ComeBack вашей команде
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
            <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-400">
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
            <p className="pt-1 text-xs text-slate-400">
              Технологический стек, деплой, SSL и интеграции уже настроены на
              стороне admin.comeback.uz — остаётся адаптировать под ваш кейс.
            </p>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-800/70 bg-slate-950/95">
        <div className="container-page flex flex-col gap-3 py-5 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <span>© {new Date().getFullYear()} ComeBack. Все права защищены.</span>
          <div className="flex flex-wrap items-center gap-3">
            <a
              href="mailto:admin@comeback.uz"
              className="text-slate-400 underline-offset-2 hover:text-emerald-300 hover:underline"
            >
              Связаться с нами
            </a>
            <span className="hidden h-1 w-1 rounded-full bg-slate-700 sm:inline-block" />
            <span className="text-slate-500">
              Админ‑панель:{" "}
              <a
                href="https://admin.comeback.uz"
                className="text-slate-300 underline-offset-2 hover:text-emerald-300 hover:underline"
              >
                admin.comeback.uz
              </a>
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

