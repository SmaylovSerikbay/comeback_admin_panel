# 🔧 Payment Gateway Troubleshooting

## Частые проблемы и решения

### 1. Unity: "Endpoint unavailable"

**Симптомы:**
```
[ARPaymentController] ❌ Ошибка: Endpoint unavailable - check server settings
```

**Причины:**
- Неправильный URL сервера в Unity коде
- Сервер недоступен
- Проблемы с SSL/TLS
- CORS блокировка

**Решение:**

1. **Проверьте URL в Unity:**
```csharp
// Должно быть:
private string serverUrl = "https://admin.comeback.uz";
// НЕ:
// private string serverUrl = "http://89.39.95.247";
```

2. **Проверьте доступность сервера:**
```bash
curl https://admin.comeback.uz/payment-gateway/api/unity/health/
```

3. **Проверьте переменные окружения:**
```bash
cat .env | grep SITE_URL
# Должно быть:
# SITE_URL=https://admin.comeback.uz
```

---

### 2. FreedomPay: "Invalid signature"

**Симптомы:**
```
❌ Некорректная подпись CHECK/RESULT
```

**Причины:**
- Неправильный SECRET_KEY
- Неправильный MERCHANT_ID
- Проблемы с генерацией подписи

**Решение:**

1. **Проверьте настройки в .env:**
```env
FREEDOMPAY_MERCHANT_ID=552170
FREEDOMPAY_SECRET_KEY=wUQ18x3bzP86MUzn
```

2. **Проверьте логи:**
```bash
docker-compose logs web | grep signature
```

3. **Перезапустите контейнеры:**
```bash
docker-compose restart web
```

---

### 3. Docker: "Container не запускается"

**Симптомы:**
```
docker-compose ps
# web контейнер в статусе "Exit"
```

**Причины:**
- Ошибки в .env файле
- Проблемы с базой данных
- Ошибки в коде

**Решение:**

1. **Проверьте логи:**
```bash
docker-compose logs web
```

2. **Проверьте .env файл:**
```bash
nano .env
# Убедитесь что все переменные заполнены
```

3. **Пересоздайте контейнеры:**
```bash
docker-compose down
docker-compose up -d --build
```

---

### 4. Nginx: "502 Bad Gateway"

**Симптомы:**
- Браузер показывает 502 ошибку
- Unity не может подключиться

**Причины:**
- Web контейнер не запущен
- Проблемы с proxy_pass
- Неправильная конфигурация nginx

**Решение:**

1. **Проверьте статус контейнеров:**
```bash
docker-compose ps
```

2. **Проверьте nginx конфигурацию:**
```bash
docker-compose exec nginx nginx -t
```

3. **Перезапустите nginx:**
```bash
docker-compose restart nginx
```

---

### 5. SSL: "Certificate error"

**Симптомы:**
- Unity выдает SSL ошибку
- Браузер предупреждает о небезопасном соединении

**Причины:**
- Истек срок действия сертификата
- Сертификат не установлен
- Неправильный путь к сертификату

**Решение:**

1. **Обновите сертификат:**
```bash
docker-compose run --rm certbot renew
```

2. **Проверьте наличие сертификата:**
```bash
ls -la nginx/ssl/live/admin.comeback.uz-0001/
```

3. **Перезапустите nginx:**
```bash
docker-compose restart nginx
```

---

### 6. База данных: "Connection refused"

**Симптомы:**
```
django.db.utils.OperationalError: could not connect to server
```

**Причины:**
- PostgreSQL контейнер не запущен
- Неправильные credentials
- Проблемы с сетью Docker

**Решение:**

1. **Проверьте статус PostgreSQL:**
```bash
docker-compose ps db
```

2. **Проверьте подключение:**
```bash
docker-compose exec db pg_isready -U comeback_user
```

3. **Проверьте credentials в .env:**
```env
POSTGRES_USER=comeback_user
POSTGRES_PASSWORD=comeback_password_2025
POSTGRES_DB=comeback_admin
```

---

### 7. Платеж завис в статусе "pending"

**Симптомы:**
- Платеж создан, но статус не обновляется
- Unity бесконечно ждет результата

**Причины:**
- FreedomPay не отправил callback
- Callback заблокирован firewall
- Неправильный callback URL

**Решение:**

1. **Проверьте callbacks в админке:**
```
https://admin.comeback.uz/admin/payment_gateway/paymentcallback/
```

2. **Проверьте логи:**
```bash
docker-compose logs web | grep callback
```

3. **Вручную обновите статус через Django shell:**
```bash
docker-compose exec web python manage.py shell
```
```python
from payment_gateway.models import PaymentTransaction
tx = PaymentTransaction.objects.get(order_id='unity_abc123')
tx.mark_as_paid()  # или tx.mark_as_failed()
```

---

## 🔍 Полезные команды для диагностики

### Проверка всех эндпоинтов:
```bash
# Health check
curl https://admin.comeback.uz/payment-gateway/api/unity/health/

# Server info
curl https://admin.comeback.uz/payment-gateway/api/unity/server-info/

# Тестовая форма (в браузере)
open https://admin.comeback.uz/payment-gateway/test/
```

### Просмотр логов в реальном времени:
```bash
# Все логи
docker-compose logs -f

# Только web
docker-compose logs -f web

# Только nginx
docker-compose logs -f nginx

# Только db
docker-compose logs -f db
```

### Мониторинг ресурсов:
```bash
# Использование CPU/RAM
docker stats

# Дисковое пространство
docker system df
```

### Очистка и перезапуск:
```bash
# Полная очистка
docker-compose down -v
docker system prune -a -f

# Пересборка с нуля
docker-compose up -d --build --force-recreate
```

---

## 📊 Endpoints для тестирования

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/payment-gateway/api/unity/health/` | GET | Проверка доступности |
| `/payment-gateway/api/unity/server-info/` | GET | Информация о сервере |
| `/payment-gateway/api/unity/create-payment/` | POST | Создание платежа |
| `/payment-gateway/api/unity/check-status/` | GET | Проверка статуса |
| `/payment-gateway/test/` | GET | Тестовая форма |
| `/payment-gateway/dashboard/` | GET | Админ дашборд |

---

## 🆘 Последний шанс

Если ничего не помогло:

1. **Сохраните логи:**
```bash
docker-compose logs > all_logs.txt
```

2. **Проверьте переменные окружения:**
```bash
docker-compose exec web env | sort > env_vars.txt
```

3. **Экспортируйте базу данных:**
```bash
docker-compose exec db pg_dump -U comeback_user comeback_admin > db_backup.sql
```

4. **Пересоздайте всё с нуля:**
```bash
docker-compose down -v
rm -rf postgres_data/
docker-compose up -d --build
```

---

## ✅ Проверочный список

После устранения проблемы проверьте:

- [ ] Health check возвращает success
- [ ] Server info показывает правильный URL
- [ ] Тестовый платеж создается
- [ ] Callback'и от FreedomPay обрабатываются
- [ ] Статус платежа обновляется
- [ ] Unity успешно подключается
- [ ] Логи не показывают ошибок

---

**Последнее обновление:** 2025-01-10  
**Версия:** 1.0
