# 🔧 Обновление URL сервера в Unity

## Проблема

Unity приложение использует **старый URL** `http://89.39.95.247`, из-за чего:
- POST на create-payment возвращает **500 Internal Server Error**
- Отображается: `[ARPaymentController] ❌ Ошибка: Endpoint unavailable - check server settings`

## Решение

### 1. Обновите URL в FreedomPayManager.cs

**Файл:** `Assets/PaymentSystem/FreedomPayManager.cs`

Найдите переменную `serverUrl` и измените:

```csharp
// ❌ СТАРЫЙ (не работает после смены сервера):
private string serverUrl = "http://89.39.95.247";

// ✅ НОВЫЙ (используйте домен с HTTPS):
private string serverUrl = "https://admin.comeback.uz";
```

**Если у вас новый IP сервера:**
```csharp
private string serverUrl = "https://НОВЫЙ_IP";  // или http:// если без SSL
```

### 2. Проверьте другие места с URL

Поищите в проекте Unity по строкам:
- `89.39.95.247`
- `http://89.39.95.247`
- `serverUrl`
- `baseUrl`
- `apiUrl`

Замените все вхождения на актуальный URL сервера.

### 3. Пересоберите приложение

После изменений:
1. Сохраните файлы
2. Пересоберите проект (Build)
3. Установите новую версию на устройство

---

## Диагностика 500 ошибки на сервере

Если после обновления URL ошибка 500 сохраняется:

1. **Проверьте логи Django на сервере:**
   ```bash
   docker-compose logs -f web
   ```
   При создании платежа в логах появится точная ошибка.

2. **Проверьте миграции:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Проверьте .env на сервере:**
   - `SITE_URL` — должен соответствовать вашему домену
   - `FREEDOMPAY_MERCHANT_ID` и `FREEDOMPAY_SECRET_KEY` — должны быть заданы

4. **Тест через curl:**
   ```bash
   curl -X POST https://admin.comeback.uz/payment-gateway/api/unity/create-payment/ \
     -H "Content-Type: application/json" \
     -d '{"unity_user_id":"test123","amount":5000,"description":"Test"}'
   ```
