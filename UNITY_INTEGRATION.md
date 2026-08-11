# 🎮 Unity интеграция с Payment Gateway

## ❌ Проблема после смены сервера

После смены сервера Unity приложение выдавало ошибку:
```
[ARPaymentController] ❌ Ошибка: Endpoint unavailable - check server settings
```

## ✅ Решение

### 1. Обновленные переменные окружения

Добавлены новые переменные в `.env`:
```env
# Server URLs
SITE_URL=https://admin.comeback.uz
SITE_DOMAIN=admin.comeback.uz
USE_HTTPS=True

# FreedomPay Settings
FREEDOMPAY_MERCHANT_ID=552170
FREEDOMPAY_SECRET_KEY=wUQ18x3bzP86MUzn
```

### 2. Новые endpoints для диагностики

#### Health Check (проверка доступности)
```
GET https://admin.comeback.uz/payment-gateway/api/unity/health/
```

**Ответ:**
```json
{
  "success": true,
  "status": "healthy",
  "server_time": "2025-01-10T12:30:45.123456+05:00",
  "base_url": "https://admin.comeback.uz",
  "endpoints": {
    "create_payment": "https://admin.comeback.uz/payment-gateway/api/unity/create-payment/",
    "check_status": "https://admin.comeback.uz/payment-gateway/api/unity/check-status/"
  },
  "version": "1.0",
  "merchant_id": "552170"
}
```

#### Server Info (информация о сервере)
```
GET https://admin.comeback.uz/payment-gateway/api/unity/server-info/
```

**Ответ:**
```json
{
  "success": true,
  "server_info": {
    "base_url": "https://admin.comeback.uz",
    "site_url": "https://admin.comeback.uz",
    "domain": "admin.comeback.uz",
    "use_https": true,
    "protocol": "https"
  },
  "endpoints": {
    "create_payment": "https://admin.comeback.uz/payment-gateway/api/unity/create-payment/",
    "check_status": "https://admin.comeback.uz/payment-gateway/api/unity/check-status/",
    "health_check": "https://admin.comeback.uz/payment-gateway/api/unity/health/",
    "server_info": "https://admin.comeback.uz/payment-gateway/api/unity/server-info/"
  },
  "freedompay": {
    "merchant_id": "552170",
    "success_url": "https://admin.comeback.uz/payment-gateway/freedompay/success/",
    "fail_url": "https://admin.comeback.uz/payment-gateway/freedompay/fail/"
  },
  "server_time": "2025-01-10T12:30:45.123456+05:00",
  "version": "1.0"
}
```

## 🔧 Изменения в Unity коде

### До (старый код с проблемой):
```csharp
// FreedomPayManager.cs
private string serverUrl = "http://89.39.95.247"; // ❌ Старый IP адрес
```

### После (правильный код):
```csharp
// FreedomPayManager.cs
private string serverUrl = "https://admin.comeback.uz"; // ✅ Новый домен с HTTPS

// Или использовать IP адрес (если домен недоступен):
// private string serverUrl = "http://89.39.95.247";
```

### Пример проверки подключения в Unity:

```csharp
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class FreedomPayManager : MonoBehaviour
{
    // ✅ Правильный URL сервера
    private string serverUrl = "https://admin.comeback.uz";
    
    // Альтернативный вариант для тестирования
    // private string serverUrl = "http://89.39.95.247";
    
    private string createPaymentEndpoint => $"{serverUrl}/payment-gateway/api/unity/create-payment/";
    private string checkStatusEndpoint => $"{serverUrl}/payment-gateway/api/unity/check-status/";
    private string healthCheckEndpoint => $"{serverUrl}/payment-gateway/api/unity/health/";
    
    void Start()
    {
        // Проверяем доступность сервера при старте
        StartCoroutine(CheckServerHealth());
    }
    
    /// <summary>
    /// Проверка доступности сервера
    /// </summary>
    IEnumerator CheckServerHealth()
    {
        Debug.Log($"🔍 Проверка доступности сервера: {healthCheckEndpoint}");
        
        using (UnityWebRequest request = UnityWebRequest.Get(healthCheckEndpoint))
        {
            // Устанавливаем таймаут
            request.timeout = 10;
            
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                string responseText = request.downloadHandler.text;
                Debug.Log($"✅ Сервер доступен: {responseText}");
                
                // Парсим ответ
                ServerHealthResponse response = JsonUtility.FromJson<ServerHealthResponse>(responseText);
                
                if (response.success)
                {
                    Debug.Log($"✅ Server Status: {response.status}");
                    Debug.Log($"✅ Base URL: {response.base_url}");
                    Debug.Log($"✅ Merchant ID: {response.merchant_id}");
                }
            }
            else
            {
                Debug.LogError($"❌ Ошибка подключения к серверу: {request.error}");
                Debug.LogError($"❌ Response Code: {request.responseCode}");
                Debug.LogError($"❌ Endpoint: {healthCheckEndpoint}");
                
                // Попытка альтернативного подключения
                TryAlternativeConnection();
            }
        }
    }
    
    /// <summary>
    /// Попытка подключения к альтернативному адресу
    /// </summary>
    void TryAlternativeConnection()
    {
        string alternativeUrl = "http://89.39.95.247";
        Debug.Log($"🔄 Попытка подключения к альтернативному адресу: {alternativeUrl}");
        
        serverUrl = alternativeUrl;
        StartCoroutine(CheckServerHealth());
    }
    
    /// <summary>
    /// Создание платежа
    /// </summary>
    public IEnumerator CreatePayment(string unityUserId, int amount, string description)
    {
        Debug.Log($"💳 Создание платежа: {amount} UZS для пользователя {unityUserId}");
        
        // Создаем JSON данные
        PaymentRequest paymentData = new PaymentRequest
        {
            unity_user_id = unityUserId,
            amount = amount,
            description = description
        };
        
        string jsonData = JsonUtility.ToJson(paymentData);
        
        using (UnityWebRequest request = new UnityWebRequest(createPaymentEndpoint, "POST"))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            request.timeout = 15;
            
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                string responseText = request.downloadHandler.text;
                Debug.Log($"✅ Платеж создан: {responseText}");
                
                PaymentResponse response = JsonUtility.FromJson<PaymentResponse>(responseText);
                
                if (response.success)
                {
                    Debug.Log($"✅ Order ID: {response.order_id}");
                    Debug.Log($"✅ Payment URL: {response.payment_url}");
                    
                    // Открываем браузер для оплаты
                    Application.OpenURL(response.payment_url);
                    
                    // Начинаем проверку статуса
                    StartCoroutine(CheckPaymentStatus(response.order_id));
                }
            }
            else
            {
                Debug.LogError($"❌ Ошибка создания платежа: {request.error}");
                Debug.LogError($"❌ Response Code: {request.responseCode}");
                Debug.LogError($"❌ Response: {request.downloadHandler.text}");
            }
        }
    }
    
    /// <summary>
    /// Проверка статуса платежа
    /// </summary>
    public IEnumerator CheckPaymentStatus(string orderId)
    {
        string url = $"{checkStatusEndpoint}?order_id={orderId}";
        
        // Проверяем статус каждые 3 секунды
        for (int i = 0; i < 60; i++) // 3 минуты максимум
        {
            yield return new WaitForSeconds(3f);
            
            Debug.Log($"🔍 Проверка статуса платежа #{i + 1}: {orderId}");
            
            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                request.timeout = 10;
                
                yield return request.SendWebRequest();
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    string responseText = request.downloadHandler.text;
                    PaymentStatusResponse response = JsonUtility.FromJson<PaymentStatusResponse>(responseText);
                    
                    if (response.success)
                    {
                        Debug.Log($"📊 Статус платежа: {response.status}");
                        
                        if (response.status == "success")
                        {
                            Debug.Log("✅ Платеж успешно выполнен!");
                            OnPaymentSuccess(orderId);
                            yield break;
                        }
                        else if (response.status == "failed")
                        {
                            Debug.LogWarning("❌ Платеж отклонен");
                            OnPaymentFailed("Payment was declined");
                            yield break;
                        }
                    }
                }
                else
                {
                    Debug.LogWarning($"⚠️ Ошибка проверки статуса: {request.error}");
                }
            }
        }
        
        Debug.LogWarning("⏱️ Таймаут проверки статуса платежа");
        OnPaymentFailed("Timeout checking payment status");
    }
    
    void OnPaymentSuccess(string orderId)
    {
        Debug.Log($"🎉 Платеж успешен: {orderId}");
        // Ваша логика при успешном платеже
    }
    
    void OnPaymentFailed(string reason)
    {
        Debug.LogError($"❌ Платеж не выполнен: {reason}");
        // Ваша логика при неудачном платеже
    }
}

// Классы для сериализации JSON
[System.Serializable]
public class ServerHealthResponse
{
    public bool success;
    public string status;
    public string server_time;
    public string base_url;
    public string merchant_id;
}

[System.Serializable]
public class PaymentRequest
{
    public string unity_user_id;
    public int amount;
    public string description;
}

[System.Serializable]
public class PaymentResponse
{
    public bool success;
    public string order_id;
    public string session_id;
    public string payment_url;
    public int amount;
    public string currency;
    public string error;
}

[System.Serializable]
public class PaymentStatusResponse
{
    public bool success;
    public string order_id;
    public string status;
    public int amount;
    public string currency;
    public string created_at;
    public string paid_at;
    public string error;
}
```

## 🚀 Инструкции по развертыванию

### 1. Обновите переменные окружения на сервере

```bash
ssh root@89.39.95.247
cd comeback_admin_panel

# Отредактируйте .env файл
nano .env
```

Добавьте/обновите:
```env
SITE_URL=https://admin.comeback.uz
SITE_DOMAIN=admin.comeback.uz
USE_HTTPS=True
FREEDOMPAY_MERCHANT_ID=552170
FREEDOMPAY_SECRET_KEY=wUQ18x3bzP86MUzn
```

### 2. Перезапустите Docker контейнеры

```bash
docker-compose down
docker-compose up -d --build
```

### 3. Проверьте endpoints

```bash
# Health check
curl https://admin.comeback.uz/payment-gateway/api/unity/health/

# Server info
curl https://admin.comeback.uz/payment-gateway/api/unity/server-info/
```

### 4. Обновите Unity приложение

Измените `serverUrl` в `FreedomPayManager.cs`:
```csharp
private string serverUrl = "https://admin.comeback.uz";
```

## 🔍 Диагностика проблем

### Проблема 1: "Endpoint unavailable"

**Причина:** Unity не может подключиться к серверу

**Решение:**
1. Проверьте доступность сервера: `curl https://admin.comeback.uz/payment-gateway/api/unity/health/`
2. Убедитесь, что Docker контейнеры запущены: `docker-compose ps`
3. Проверьте логи: `docker-compose logs web`
4. Проверьте URL в Unity коде

### Проблема 2: SSL/TLS ошибки

**Причина:** Проблемы с SSL сертификатом

**Решение для разработки:**
```csharp
// В Unity можно временно отключить проверку SSL
ServicePointManager.ServerCertificateValidationCallback = 
    (sender, certificate, chain, sslPolicyErrors) => true;
```

**Решение для production:**
1. Обновите SSL сертификат: `docker-compose run --rm certbot renew`
2. Перезапустите nginx: `docker-compose restart nginx`

### Проблема 3: CORS ошибки

**Причина:** Nginx блокирует запросы от Unity

**Решение:** CORS уже настроены в `nginx.conf`, но убедитесь что контейнер перезапущен

## 📝 Доступные URL варианты

### Production (рекомендуется):
```
https://admin.comeback.uz
```

### Development/Fallback:
```
http://89.39.95.247
```

## ✅ Чеклист после обновления

- [ ] Обновлены переменные окружения в `.env`
- [ ] Docker контейнеры перезапущены
- [ ] Health check возвращает success
- [ ] Unity код обновлен с новым URL
- [ ] Тестовый платеж успешно создается
- [ ] Статус платежа корректно отслеживается

## 📞 Поддержка

При возникновении проблем проверьте:
1. Логи Django: `docker-compose logs web`
2. Логи Nginx: `docker-compose logs nginx`
3. Health check endpoint
4. Server info endpoint
5. Unity Debug.Log для деталей ошибок

---

**Версия:** 1.0  
**Дата обновления:** 2025-01-10  
**Статус:** ✅ Готово к использованию
