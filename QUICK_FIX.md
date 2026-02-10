# 🚨 БЫСТРОЕ ИСПРАВЛЕНИЕ: Unity Payment Gateway Error

## ❌ Ошибка
```
[ARPaymentController] ❌ Ошибка: Endpoint unavailable - check server settings
```

## ⚡ БЫСТРОЕ РЕШЕНИЕ (5 минут)

### ШАГ 1: Обновите сервер (на VDS)

```bash
# Подключитесь к серверу
ssh root@89.39.95.247

# Перейдите в директорию проекта
cd comeback_admin_panel

# Обновите код
git pull

# Обновите .env файл
nano .env
```

**Добавьте эти строки в .env:**
```env
SITE_URL=https://admin.comeback.uz
SITE_DOMAIN=admin.comeback.uz
USE_HTTPS=True
FREEDOMPAY_MERCHANT_ID=552170
FREEDOMPAY_SECRET_KEY=wUQ18x3bzP86MUzn
```

```bash
# Перезапустите контейнеры
docker-compose down
docker-compose up -d --build

# Проверьте что всё работает
curl https://admin.comeback.uz/payment-gateway/api/unity/health/
```

### ШАГ 2: Обновите Unity код

Найдите файл `FreedomPayManager.cs` или `ARPaymentController.cs` и измените:

**БЫЛО:**
```csharp
private string serverUrl = "http://89.39.95.247";
```

**СТАЛО:**
```csharp
private string serverUrl = "https://admin.comeback.uz";
```

### ШАГ 3: Пересоберите Unity приложение

Готово! Ошибка должна исчезнуть.

---

## 🔍 ПРОВЕРКА

### Проверьте доступность сервера:

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://admin.comeback.uz/payment-gateway/api/unity/health/" | Select-Object -Expand Content
```

**Linux/Mac:**
```bash
curl https://admin.comeback.uz/payment-gateway/api/unity/health/
```

**Ожидаемый ответ:**
```json
{
  "success": true,
  "status": "healthy",
  "base_url": "https://admin.comeback.uz",
  ...
}
```

---

## 🆘 ВСЁ ЕЩЁ НЕ РАБОТАЕТ?

### Вариант A: Используйте IP адрес (временное решение)

**В Unity коде:**
```csharp
private string serverUrl = "http://89.39.95.247";
```

**На сервере (.env):**
```env
SITE_URL=http://89.39.95.247
USE_HTTPS=False
```

### Вариант B: Проблемы с SSL

Если ошибка связана с SSL сертификатом, временно отключите проверку в Unity:

```csharp
void Start()
{
    // ТОЛЬКО ДЛЯ РАЗРАБОТКИ! Удалите в production!
    System.Net.ServicePointManager.ServerCertificateValidationCallback = 
        (sender, cert, chain, sslPolicyErrors) => true;
}
```

### Вариант C: Проверьте логи

**На сервере:**
```bash
# Логи Django
docker-compose logs web --tail=100

# Логи Nginx
docker-compose logs nginx --tail=100

# Все логи
docker-compose logs --tail=100 -f
```

**В Unity:**
Проверьте Console на наличие деталей ошибки.

---

## 📋 ЧЕКЛИСТ ДИАГНОСТИКИ

Пройдитесь по этому списку:

- [ ] Сервер доступен: `curl https://admin.comeback.uz/payment-gateway/api/unity/health/`
- [ ] Docker контейнеры запущены: `docker-compose ps`
- [ ] URL в Unity коде правильный (https://admin.comeback.uz)
- [ ] Переменные окружения обновлены в .env
- [ ] Контейнеры перезапущены после изменения .env
- [ ] Firewall не блокирует порты 80 и 443
- [ ] SSL сертификат актуален
- [ ] В Unity используется актуальная версия кода

---

## 🔧 ДОПОЛНИТЕЛЬНЫЕ КОМАНДЫ

### Полная перезагрузка сервера:
```bash
docker-compose down
docker system prune -f
docker-compose up -d --build
```

### Просмотр статуса сервисов:
```bash
docker-compose ps
```

### Проверка SSL сертификата:
```bash
docker-compose exec nginx nginx -t
```

### Обновление SSL сертификата:
```bash
docker-compose run --rm certbot renew
docker-compose restart nginx
```

---

## 📞 КОНТАКТЫ ПОДДЕРЖКИ

Если проблема не решена:

1. **Проверьте логи:** `docker-compose logs -f`
2. **Проверьте health check:** `curl https://admin.comeback.uz/payment-gateway/api/unity/health/`
3. **Проверьте server info:** `curl https://admin.comeback.uz/payment-gateway/api/unity/server-info/`
4. **Отправьте логи** из Unity Console и Django logs

---

## ✅ РЕШЕНО!

После выполнения этих шагов Unity должен успешно подключаться к серверу!

**Время исправления:** ~5 минут  
**Сложность:** Низкая  
**Требуется перезапуск:** Да (Docker + Unity)
