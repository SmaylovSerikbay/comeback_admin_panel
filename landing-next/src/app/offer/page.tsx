import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Публичная оферта — ComeBack",
  description:
    "Публичная оферта (договор) на предоставление доступа к AR-контенту COMEBACK.UZ. LEMALA MChJ.",
};

export default function OfferPage() {
  return (
    <div className="min-h-screen bg-slate-950">
      <div className="border-b border-slate-800/70">
        <div className="container-page flex h-14 items-center">
          <Link
            href="/"
            className="text-sm text-emerald-400 hover:text-emerald-300"
          >
            ← На главную
          </Link>
        </div>
      </div>

      <article className="container-page max-w-3xl py-10 text-sm leading-relaxed text-slate-200">
        <h1 className="mb-2 text-2xl font-semibold text-slate-50">
          ПУБЛИЧНАЯ ОФЕРТА (ДОГОВОР)
        </h1>
        <p className="mb-1 text-slate-300">
          на предоставление доступа к контенту дополненной реальности
          (AR-аттракциону)
        </p>
        <p className="mb-8 text-xs text-slate-400">
          г. Бухара · 01.04.2026 г. · LEMALA MChJ
        </p>

        <section className="space-y-3">
          <h2 className="mt-8 text-base font-semibold text-slate-50">
            1. ОБЩИЕ ПОЛОЖЕНИЯ
          </h2>
          <p>
            <strong>1.1.</strong> Настоящий документ является официальным
            предложением (Публичной офертой) LEMALA MChJ, именуемого в
            дальнейшем «Исполнитель», для любого физического лица (далее —
            «Пользователь»), которое примет настоящее предложение на указанных
            ниже условиях.
          </p>
          <p>
            <strong>1.2.</strong> Акцептом (принятием) данной Оферты является
            факт оплаты доступа к платному контенту в мобильном приложении
            COMEBACK.UZ (далее — «Приложение»). С момента оплаты договор
            считается заключенным.
          </p>

          <h2 className="mt-8 text-base font-semibold text-slate-50">
            2. ПРЕДМЕТ ДОГОВОРА
          </h2>
          <p>
            <strong>2.1.</strong> Исполнитель предоставляет Пользователю на
            возмездной основе право доступа к просмотру цифровых объектов
            (персонажей древности) с использованием технологии дополненной
            реальности (AR) в определенных географических локациях (туристических
            площадях).
          </p>
          <p>
            <strong>2.2.</strong> Услуга носит характер цифрового интерактивного
            аттракциона (зрелища), предоставляемого в режиме реального времени.
          </p>

          <h2 className="mt-8 text-base font-semibold text-slate-50">
            3. ПОРЯДОК ОКАЗАНИЯ УСЛУГ
          </h2>
          <p>
            <strong>3.1.</strong> Доступ к AR-контенту открывается Пользователю
            немедленно после подтверждения транзакции платежной системой
            (локальные платежные системы).
          </p>
          <p>
            <strong>3.2.</strong> Для использования Приложения Пользователь
            обязан обеспечить наличие:
          </p>
          <ul className="list-disc space-y-1 pl-5">
            <li>
              смартфона с поддержкой технологий AR (ARCore/ARKit);
            </li>
            <li>активного интернет-соединения;</li>
            <li>
              включенного модуля GPS/ГЛОНАСС для определения местоположения на
              площади.
            </li>
          </ul>
          <p>
            <strong>3.3.</strong> Момент оказания услуги: Услуга считается
            оказанной в полном объеме и принятой Пользователем в момент
            предоставления технического доступа к платному AR-контенту в
            интерфейсе Приложения.
          </p>

          <h2 className="mt-8 text-base font-semibold text-slate-50">
            4. СТОИМОСТЬ И ПОРЯДОК ОПЛАТЫ
          </h2>
          <p>
            <strong>4.1.</strong> Стоимость доступа (Билета на
            AR-аттракцион) указывается непосредственно в интерфейсе Приложения
            перед моментом совершения оплаты.
          </p>
          <p>
            <strong>4.2.</strong> Оплата производится через встроенные покупки
            (In-App Purchases) или иные доступные платежные методы.
          </p>

          <h2 className="mt-8 text-base font-semibold text-slate-50">
            5. УСЛОВИЯ ОТКАЗА И ВОЗВРАТА СРЕДСТВ
          </h2>
          <p>
            <strong>5.1.</strong> В соответствии со спецификой цифрового
            контента и ст. 18 Закона РУз «О защите прав потребителей», возврат
            денежных средств за оказанную услугу (предоставленный доступ) не
            производится, так как услуга имеет характер разового зрелищного
            мероприятия, потребляемого в момент предоставления доступа.
          </p>
          <p>
            <strong>5.2.</strong> Пользователь подтверждает, что ознакомлен с
            демонстрационной версией (если имеется) или техническими требованиями
            Приложения до момента оплаты. Субъективная оценка «не понравилось
            качество персонажа» или «ожидал другого» не является основанием для
            возврата.
          </p>
          <p>
            <strong>5.3.</strong> Возврат возможен исключительно в случае
            доказанной технической неисправности Приложения на стороне
            Исполнителя, препятствующей просмотру контента, при условии, что
            устройство Пользователя полностью соответствует системным
            требованиям.
          </p>

          <h2 className="mt-8 text-base font-semibold text-slate-50">
            6. ОТВЕТСТВЕННОСТЬ СТОРОН
          </h2>
          <p>
            <strong>6.1.</strong> Исполнитель не несет ответственности за:
          </p>
          <ul className="list-disc space-y-1 pl-5">
            <li>
              некорректную работу GPS из-за погодных условий или застройки;
            </li>
            <li>
              ограничения доступа к площадям со стороны государственных органов;
            </li>
            <li>
              несоблюдение Пользователем мер безопасности при перемещении в
              пространстве во время просмотра AR-контента.
            </li>
          </ul>
          <p>
            <strong>6.2.</strong> Пользователь обязуется соблюдать осторожность,
            не создавать помех другим туристам и следить за окружающей
            обстановкой во время использования Приложения.
          </p>

          <h2 className="mt-8 text-base font-semibold text-slate-50">
            7. ИНТЕЛЛЕКТУАЛЬНАЯ СОБСТВЕННОСТЬ
          </h2>
          <p>
            <strong>7.1.</strong> Все AR-модели, анимации и звуковое
            сопровождение являются интеллектуальной собственностью Исполнителя.
            Запрещается любая запись экрана с целью дальнейшего коммерческого
            использования контента без разрешения правообладателя.
          </p>

          <h2 className="mt-8 text-base font-semibold text-slate-50">
            8. РЕКВИЗИТЫ ИСПОЛНИТЕЛЯ
          </h2>
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4 text-slate-200">
            <p className="font-semibold text-slate-50">LEMALA MChJ</p>
            <p>Р/С 2020 8000 9070 4094 9002</p>
            <p>МФО 00450</p>
            <p>ИНН: 310316898</p>
            <p>
              Адрес: БУХАРСКАЯ ОБЛАСТЬ БУХАРСКИЙ РАЙОН, Шехонча МФЙ, Тутихушк
              кучаси, 16-уй
            </p>
            <p>Телефон: +998 99 707 7074</p>
            <p>E-mail: hello@comeback.uz</p>
          </div>
        </section>

        <hr className="my-12 border-slate-800" />

        <section className="space-y-3 text-slate-300">
          <h2 className="text-xl font-semibold text-slate-50">
            Public Offer (English)
          </h2>
          <p className="text-xs text-slate-500">
            The following is an English summary for convenience. In case of
            discrepancy, the Russian text above prevails.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            1. General provisions
          </h3>
          <p>
            <strong>1.1.</strong> This document constitutes an official proposal
            (Public Offer) by LEMALA MChJ, hereinafter referred to as the
            &quot;Contractor,&quot; to any individual (hereinafter referred to as
            the &quot;User&quot;) who accepts this proposal under the terms
            specified below.
          </p>
          <p>
            <strong>1.2.</strong> Acceptance of this Offer is effected by the act
            of paying for access to paid content within the COMEBACK.UZ mobile
            application (hereinafter referred to as the &quot;Application&quot;).
          </p>
          <p>
            <strong>1.3.</strong> The agreement is considered concluded from the
            moment of payment.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            2. Subject of the agreement
          </h3>
          <p>
            <strong>2.1.</strong> The Contractor provides the User, for a fee,
            the right of access to view digital objects (ancient characters)
            using augmented reality (AR) technology at specific geographic
            locations (tourist squares).
          </p>
          <p>
            <strong>2.2.</strong> The service is characterized as a digital
            interactive attraction (spectacle) provided in real-time.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            3. Service provision procedure
          </h3>
          <p>
            <strong>3.1.</strong> Access to AR content is granted to the User
            immediately after the transaction is confirmed by the payment system
            (local payment systems).
          </p>
          <p>
            <strong>3.2.</strong> To use the Application, the User must ensure
            they have: a smartphone supporting AR technologies (ARCore/ARKit); an
            active internet connection; an enabled GPS/GLONASS module to
            determine location on the square.
          </p>
          <p>
            <strong>3.3.</strong> Moment of service delivery: The service is
            considered fully rendered and accepted by the User at the moment
            technical access to the paid AR content is provided within the
            Application interface.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            4. Cost and payment procedure
          </h3>
          <p>
            <strong>4.1.</strong> The cost of access (Ticket to the AR
            Attraction) is indicated directly in the Application interface prior
            to payment.
          </p>
          <p>
            <strong>4.2.</strong> Payment is made via in-app purchases or other
            available payment methods.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            5. Cancellation and refund terms
          </h3>
          <p>
            <strong>5.1.</strong> In accordance with the specifics of digital
            content and Article 18 of the Law of the Republic of Uzbekistan
            &quot;On the Protection of Consumer Rights,&quot; no refund shall be
            issued for the rendered service (provided access), as the service is
            a one-time entertainment event consumed at the moment access is
            granted.
          </p>
          <p>
            <strong>5.2.</strong> The User confirms they have reviewed the demo
            version (if available) or the technical requirements of the
            Application before payment.
          </p>
          <p>
            <strong>5.3.</strong> Subjective assessments such as &quot;disliked
            the character quality&quot; or &quot;expected something else&quot; do
            not constitute grounds for a refund.
          </p>
          <p>
            <strong>5.4.</strong> A refund is possible only in the event of a
            proven technical malfunction of the Application on the
            Contractor&apos;s side that prevents viewing the content, provided
            the User&apos;s device fully meets the system requirements.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            6. Liability of the parties
          </h3>
          <p>
            <strong>6.1.</strong> The Contractor is not liable for: inaccurate GPS
            performance due to weather conditions or urban structures; access
            restrictions to squares imposed by government authorities; the
            User&apos;s failure to observe safety measures while moving in space
            during AR content viewing.
          </p>
          <p>
            <strong>6.2.</strong> The User agrees to exercise caution, avoid
            creating obstacles for other tourists, and remain aware of their
            surroundings while using the Application.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            7. Intellectual property
          </h3>
          <p>
            <strong>7.1.</strong> All AR models, animations, and audio
            accompaniment are the intellectual property of the Contractor.
          </p>
          <p>
            <strong>7.2.</strong> Any screen recording for the purpose of further
            commercial use of the content without the copyright holder&apos;s
            permission is prohibited.
          </p>

          <h3 className="mt-6 text-base font-semibold text-slate-50">
            8. Contractor details
          </h3>
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
            <p className="font-semibold text-slate-50">LEMALA MChJ</p>
            <p>TIN (INN): 310316898</p>
            <p>
              Address: 16 Tutikhushk St., Shekhoncha MFY, Bukhara District,
              Bukhara Region
            </p>
            <p>Support E-mail: hello@comeback.uz</p>
          </div>
        </section>
      </article>
    </div>
  );
}
