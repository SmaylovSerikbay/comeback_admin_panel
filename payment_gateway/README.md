# Payment Gateway - Платежный шлюз

Django приложение для интеграции Unity с платежной системой FreedomPay.

## ✅ Обновление 1.1 (2025-01-10)

**Исправлена критическая ошибка:** Unity "Endpoint unavailable - check server settings"

### Что нового:
- ✅ Гибкая конфигурация URL через переменные окружения
- ✅ Новые endpoints для диагностики (health check, server info)
- ✅ Автоматическое определение правильного протокола (HTTP/HTTPS)
- ✅ Подробная документация по интеграции Unity
- ✅ Руководства по устранению неполадок

## Возможности

- ✅ Создание платежей через Unity API
- ✅ Проверка статуса платежей
- ✅ Автоматическая обработка callback'ов от FreedomPay
- ✅ Административный дашборд для мониторинга
- ✅ Полная интеграция с Django Admin
- ✅ Логирование всех операций
- ✅ Health check для проверки доступности сервера
- ✅ Server info endpoint для получения конфигурации

## Установка

1. Приложение уже добавлено в `INSTALLED_APPS`
2. URL'ы подключены в основном `urls.py`
3. Выполните миграции: `python manage.py makemigrations payment_gateway && python manage.py migrate`

## API Endpoints

### Unity API

#### Health Check (НОВОЕ!)
```
GET /payment-gateway/api/unity/health/
```
Проверка доступности сервера и получение актуальных endpoints

#### Server Info (НОВОЕ!)
```
GET /payment-gateway/api/unity/server-info/
```
Получение полной информации о конфигурации сервера

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

### Быстрый старт:

```csharp
// В FreedomPayManager.cs
private string serverUrl = "https://admin.comeback.uz";

void Start()
{
    StartCoroutine(CheckServerHealth());
}

IEnumerator CheckServerHealth()
{
    string healthUrl = serverUrl + "/payment-gateway/api/unity/health/";
    using (UnityWebRequest request = UnityWebRequest.Get(healthUrl))
    {
        yield return request.SendWebRequest();
        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("✅ Server available: " + request.downloadHandler.text);
        }
        else
        {
            Debug.LogError("❌ Server unavailable: " + request.error);
        }
    }
}
```

### Полная документация:
- **UNITY_INTEGRATION.md** - детальное руководство по интеграции
- **QUICK_FIX.md** - быстрое исправление проблем
- **TROUBLESHOOTING.md** - устранение неполадок

## Настройка FreedomPay

### Переменные окружения (.env):
```env
SITE_URL=https://admin.comeback.uz
SITE_DOMAIN=admin.comeback.uz
USE_HTTPS=True
FREEDOMPAY_MERCHANT_ID=552170
FREEDOMPAY_SECRET_KEY=wUQ18x3bzP86MUzn
```

### Callback URLs в настройках FreedomPay:
- Check: `https://admin.comeback.uz/payment-gateway/freedompay/check/`
- Result: `https://admin.comeback.uz/payment-gateway/freedompay/result/`
- Success: `https://admin.comeback.uz/payment-gateway/freedompay/success/`
- Fail: `https://admin.comeback.uz/payment-gateway/freedompay/fail/`

## Логирование

Все операции логируются с временными метками. Логи доступны в консоли Django и в файлах логов.

## Безопасность

- CSRF защита отключена для callback'ов FreedomPay
- Проверка подписи всех входящих запросов
- Валидация входных данных
- Авторизация для административных функций
- Credentials хранятся в переменных окружения
- Поддержка HTTPS для защищенных соединений

## Миграция с версии 1.0

Если у вас возникла ошибка **"Endpoint unavailable"** после смены сервера:

1. Прочитайте **QUICK_FIX.md** для быстрого решения (5 минут)
2. Следуйте **DEPLOYMENT_STEPS.md** для пошаговой инструкции
3. Изучите **TROUBLESHOOTING.md** если проблема не решена

## Документация

- **README.md** (этот файл) - общая информация
- **UNITY_INTEGRATION.md** - интеграция с Unity
- **QUICK_FIX.md** - быстрое исправление ошибки endpoint
- **TROUBLESHOOTING.md** - устранение неполадок
- **CHANGELOG_PAYMENT_FIX.md** - журнал изменений
- **DEPLOYMENT_STEPS.md** - пошаговое развертывание
