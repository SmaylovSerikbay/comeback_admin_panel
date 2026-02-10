# 🚀 Пошаговая инструкция по развертыванию исправлений

## Цель
Устранить ошибку Unity "Endpoint unavailable - check server settings" после смены сервера.

---

## ⏱️ Время выполнения: ~10 минут

---

## 📋 ЧАСТЬ 1: Обновление сервера (5 минут)

### Шаг 1.1: Подключитесь к серверу
```bash
ssh root@89.39.95.247
```

### Шаг 1.2: Перейдите в директорию проекта
```bash
cd comeback_admin_panel
```

### Шаг 1.3: Сделайте резервную копию текущего .env
```bash
cp .env .env.backup_$(date +%Y%m%d_%H%M%S)
```

### Шаг 1.4: Обновите код из репозитория
```bash
git pull origin main
```

Если возникла ошибка с локальными изменениями:
```bash
git stash
git pull origin main
```

### Шаг 1.5: Обновите .env файл
```bash
nano .env
```

**Найдите и обновите/добавьте следующие строки:**

```env
# Django Settings
DEBUG=False
SECRET_KEY=django-insecure-production-secret-key-2025-change-this
ALLOWED_HOSTS=admin.comeback.uz,89.39.95.247,localhost,127.0.0.1

# Server URLs (НОВЫЕ ПЕРЕМЕННЫЕ!)
SITE_URL=https://admin.comeback.uz
SITE_DOMAIN=admin.comeback.uz
USE_HTTPS=True

# FreedomPay Settings (НОВЫЕ ПЕРЕМЕННЫЕ!)
FREEDOMPAY_MERCHANT_ID=552170
FREEDOMPAY_SECRET_KEY=wUQ18x3bzP86MUzn

# Database
POSTGRES_DB=comeback_admin
POSTGRES_USER=comeback_user
POSTGRES_PASSWORD=comeback_password_2025
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECURE_SSL_REDIRECT=False

# Остальные переменные Firebase остаются без изменений...
```

**Сохраните файл:**
- Нажмите `Ctrl + X`
- Нажмите `Y`
- Нажмите `Enter`

### Шаг 1.6: Остановите контейнеры
```bash
docker-compose down
```

### Шаг 1.7: Пересоберите и запустите контейнеры
```bash
docker-compose up -d --build
```

### Шаг 1.8: Проверьте статус контейнеров
```bash
docker-compose ps
```

**Ожидаемый результат:** Все контейнеры в статусе "Up"

### Шаг 1.9: Проверьте логи (опционально)
```bash
docker-compose logs web --tail=50
```

**Не должно быть критических ошибок**

### Шаг 1.10: Проверьте health check
```bash
curl https://admin.comeback.uz/payment-gateway/api/unity/health/
```

**Ожидаемый ответ:**
```json
{
  "success": true,
  "status": "healthy",
  ...
}
```

Если ответ успешен - переходите к Части 2!

---

## 🎮 ЧАСТЬ 2: Обновление Unity кода (5 минут)

### Шаг 2.1: Откройте Unity проект

### Шаг 2.2: Найдите файл FreedomPayManager.cs

**Обычно находится в:**
- `Assets/PaymentSystem/FreedomPayManager.cs`
- `Assets/Scripts/FreedomPayManager.cs`
- `Assets/scripts/FreedomPayManager.cs`

### Шаг 2.3: Найдите строку с serverUrl

**Найдите что-то похожее на:**
```csharp
private string serverUrl = "http://89.39.95.247";
```

**ИЛИ:**
```csharp
private string baseUrl = "http://89.39.95.247";
```

**ИЛИ:**
```csharp
public string apiUrl = "http://89.39.95.247";
```

### Шаг 2.4: Замените на новый URL

**БЫЛО:**
```csharp
private string serverUrl = "http://89.39.95.247";
```

**СТАЛО:**
```csharp
private string serverUrl = "https://admin.comeback.uz";
```

### Шаг 2.5: (Опционально) Добавьте health check при старте

**Добавьте в начало класса:**
```csharp
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
            Debug.Log("✅ Server is available: " + request.downloadHandler.text);
        }
        else
        {
            Debug.LogError("❌ Server is unavailable: " + request.error);
        }
    }
}
```

### Шаг 2.6: Сохраните файл

### Шаг 2.7: Пересоберите Unity приложение

---

## ✅ ЧАСТЬ 3: Проверка работоспособности (2 минуты)

### Шаг 3.1: Проверьте сервер

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://admin.comeback.uz/payment-gateway/api/unity/health/" | Select-Object -Expand Content
```

**Linux/Mac:**
```bash
curl https://admin.comeback.uz/payment-gateway/api/unity/health/
```

**Ожидаемый результат:**
```json
{
  "success": true,
  "status": "healthy",
  "base_url": "https://admin.comeback.uz",
  ...
}
```

### Шаг 3.2: Запустите Unity приложение

### Шаг 3.3: Попробуйте создать тестовый платеж

**В Unity Console должно появиться:**
```
✅ Server is available: {"success":true,"status":"healthy"...}
```

**А НЕ:**
```
❌ Ошибка: Endpoint unavailable - check server settings
```

### Шаг 3.4: Проверьте создание платежа

1. Запустите приложение
2. Перейдите к оплате
3. Нажмите кнопку оплаты
4. Должен открыться браузер с формой оплаты FreedomPay

---

## 🎉 ГОТОВО!

Если все шаги выполнены успешно, ошибка должна исчезнуть!

---

## 🆘 Что делать если не работает?

### Вариант A: Используйте IP адрес временно

**На сервере (.env):**
```env
SITE_URL=http://89.39.95.247
USE_HTTPS=False
```

**В Unity:**
```csharp
private string serverUrl = "http://89.39.95.247";
```

```bash
# Перезапустите Docker
docker-compose restart web
```

### Вариант B: Проверьте логи

**На сервере:**
```bash
# Логи Django
docker-compose logs web --tail=100

# Логи Nginx
docker-compose logs nginx --tail=100

# Все логи
docker-compose logs --tail=100
```

**В Unity:**
Проверьте Console на наличие подробностей ошибки

### Вариант C: Полный перезапуск

```bash
docker-compose down
docker system prune -f
docker-compose up -d --build
```

---

## 📋 Чеклист выполнения

Отметьте выполненные шаги:

### Сервер:
- [ ] Подключился к серверу
- [ ] Обновил код из репозитория
- [ ] Обновил .env файл с новыми переменными
- [ ] Перезапустил Docker контейнеры
- [ ] Проверил что контейнеры запущены
- [ ] Health check возвращает success

### Unity:
- [ ] Нашел файл FreedomPayManager.cs
- [ ] Изменил serverUrl на новый
- [ ] Добавил health check (опционально)
- [ ] Сохранил файл
- [ ] Пересобрал приложение

### Проверка:
- [ ] Сервер отвечает на health check
- [ ] Unity приложение запускается без ошибок
- [ ] Тестовый платеж создается успешно
- [ ] Браузер открывается с формой оплаты

---

## 📞 Получить помощь

Если проблема не решена:

1. **Проверьте документацию:**
   - `QUICK_FIX.md` - быстрое решение
   - `UNITY_INTEGRATION.md` - полная документация Unity
   - `payment_gateway/TROUBLESHOOTING.md` - устранение проблем

2. **Соберите информацию для отладки:**
   ```bash
   # Логи сервера
   docker-compose logs > server_logs.txt
   
   # Переменные окружения
   docker-compose exec web env | sort > env_vars.txt
   
   # Статус контейнеров
   docker-compose ps > containers_status.txt
   ```

3. **Проверьте endpoints:**
   ```bash
   curl https://admin.comeback.uz/payment-gateway/api/unity/health/
   curl https://admin.comeback.uz/payment-gateway/api/unity/server-info/
   ```

---

**Успешного развертывания! 🚀**

**Время последнего обновления:** 2025-01-10  
**Версия инструкции:** 1.0  
**Сложность:** ⭐⭐ (Средняя)
