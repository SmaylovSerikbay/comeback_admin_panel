# Payment Gateway - Платежный шлюз

Django приложение для интеграции Unity с платежной системой FreedomPay.

## Возможности

- ✅ Создание платежей через Unity API
- ✅ Проверка статуса платежей
- ✅ Автоматическая обработка callback'ов от FreedomPay
- ✅ Административный дашборд для мониторинга
- ✅ Полная интеграция с Django Admin
- ✅ Логирование всех операций

## Установка

1. Приложение уже добавлено в `INSTALLED_APPS`
2. URL'ы подключены в основном `urls.py`
3. Выполните миграции: `python manage.py makemigrations payment_gateway && python manage.py migrate`

## API Endpoints

### Unity API

#### Создание платежа
```
POST /payment-gateway/api/unity/create-payment/
Content-Type: application/json

{
    "unity_user_id": "user123",
    "amount": 1000,
    "description": "Premium subscription"
}
```

#### Проверка статуса
```
GET /payment-gateway/api/unity/check-status/?order_id=unity_abc123
```

### FreedomPay Callbacks

- `POST /payment-gateway/freedompay/check/` - Проверка заказа
- `POST /payment-gateway/freedompay/result/` - Результат платежа
- `GET/POST /payment-gateway/freedompay/success/` - Успешный платеж
- `GET/POST /payment-gateway/freedompay/fail/` - Неуспешный платеж

## Модели

### PaymentTransaction
Основная модель для хранения информации о платежах.

### PaymentCallback
Хранение callback'ов от FreedomPay.

### UnityPaymentSession
Сессии платежей для Unity пользователей.

## Администрирование

Все модели доступны в Django Admin:
- `/admin/payment_gateway/paymenttransaction/`
- `/admin/payment_gateway/paymentcallback/`
- `/admin/payment_gateway/unitypaymentsession/`

## Тестирование

- Тестовая форма: `/payment-gateway/test/`
- Дашборд: `/payment-gateway/dashboard/`
- API документация: `/payment-gateway/api-docs/`

## Unity Интеграция

Смотрите пример C# кода в API документации для интеграции с Unity.

## Настройка FreedomPay

В настройках FreedomPay укажите следующие callback URLs:
- Check: `https://comeback.uz/payment-gateway/freedompay/check/`
- Result: `https://comeback.uz/payment-gateway/freedompay/result/`
- Success: `https://comeback.uz/payment-gateway/freedompay/success/`
- Fail: `https://comeback.uz/payment-gateway/freedompay/fail/`

## Логирование

Все операции логируются с временными метками. Логи доступны в консоли Django и в файлах логов.

## Безопасность

- CSRF защита отключена для callback'ов FreedomPay
- Проверка подписи всех входящих запросов
- Валидация входных данных
- Авторизация для административных функций
