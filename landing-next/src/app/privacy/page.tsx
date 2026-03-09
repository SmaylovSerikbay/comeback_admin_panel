export default function PrivacyPage() {
  return (
    <div className="container-page max-w-3xl py-10 text-sm text-slate-100">
      <h1 className="mb-6 text-2xl font-semibold text-slate-50">
        Политика конфиденциальности
      </h1>
      <p className="mb-2 text-xs text-slate-400">
        г. Бухара, 01.01.2026 г. • COMEBACK.UZ, LEMALA MChJ
      </p>

      <section className="space-y-2">
        <h2 className="mt-6 text-base font-semibold text-slate-50">
          1. Общие положения
        </h2>
        <p>
          Настоящая Политика описывает, как приложение COMEBACK.UZ, принадлежащее
          LEMALA MChJ, собирает и использует данные Пользователя. Мы уважаем
          вашу конфиденциальность и соблюдаем законодательство Республики
          Узбекистан.
        </p>

        <h2 className="mt-6 text-base font-semibold text-slate-50">
          2. Какие данные мы собираем
        </h2>
        <ul className="list-disc space-y-1 pl-5 text-slate-200">
          <li>
            <span className="font-semibold">Камера.</span> Используется
            исключительно для визуализации дополненной реальности. Мы не
            записываем, не храним и не передаём видеопоток или фотографии с вашей
            камеры на наши серверы.
          </li>
          <li>
            <span className="font-semibold">Геопозиция (GPS).</span> Необходима
            для определения вашего местоположения на туристических площадях и
            отображения соответствующих исторических персонажей.
          </li>
          <li>
            <span className="font-semibold">Данные об устройстве.</span>{" "}
            Информация о модели смартфона и версии ОС для обеспечения
            совместимости с ARCore/ARKit.
          </li>
        </ul>

        <h2 className="mt-6 text-base font-semibold text-slate-50">
          3. Цели обработки данных
        </h2>
        <ul className="list-disc space-y-1 pl-5 text-slate-200">
          <li>предоставление технического доступа к контенту дополненной реальности;</li>
          <li>улучшение работы приложения и исправление технических неисправностей;</li>
          <li>обеспечение корректной работы GPS‑навигации в рамках цифрового аттракциона.</li>
        </ul>

        <h2 className="mt-6 text-base font-semibold text-slate-50">
          4. Передача данных третьим лицам
        </h2>
        <ul className="list-disc space-y-1 pl-5 text-slate-200">
          <li>LEMALA MChJ не продаёт и не передаёт ваши персональные данные третьим лицам.</li>
          <li>
            Обработка платежей осуществляется через сторонние платёжные системы. Мы не
            имеем доступа к данным ваших банковских карт.
          </li>
        </ul>

        <h2 className="mt-6 text-base font-semibold text-slate-50">
          5. Хранение данных
        </h2>
        <p>
          Данные о геопозиции обрабатываются в режиме реального времени и не
          сохраняются на постоянной основе после закрытия сессии в Приложении.
        </p>

        <h2 className="mt-6 text-base font-semibold text-slate-50">
          6. Ваши права
        </h2>
        <p>
          Вы можете в любой момент отозвать разрешения на доступ к камере или GPS
          в настройках своего смартфона. Однако это сделает невозможным
          использование функций дополненной реальности.
        </p>

        <h2 className="mt-6 text-base font-semibold text-slate-50">
          7. Контактная информация
        </h2>
        <p>
          По всем вопросам, связанным с конфиденциальностью, вы можете обращаться
          по адресу:
        </p>
        <p>Email: hello@comeback.uz</p>
        <p>
          Адрес: Бухарская область, Бухарский район, Шехонча МФЙ, Тутихушк
          кучаси, 16‑уй.
        </p>
      </section>
    </div>
  );
}

