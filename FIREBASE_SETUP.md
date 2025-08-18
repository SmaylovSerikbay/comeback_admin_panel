# 🔥 Настройка Firebase для Django Admin Panel

## 📋 Быстрая настройка (5 минут)

### Шаг 1: Получение Service Account ключа

1. **Откройте Firebase Console**: https://console.firebase.google.com/
2. **Выберите проект**: `comeback-2a6b2` 
3. **Перейдите в настройки**:
   - Нажмите на шестеренку ⚙️ → Project Settings
4. **Откройте вкладку Service Accounts**
5. **Создайте новый приватный ключ**:
   - Нажмите "Generate new private key"
   - Скачайте JSON файл

### Шаг 2: Настройка .env файла

Откройте файл `.env` в папке `comeback_admin_panel` и заполните:

```env
# Firebase Configuration (заполните данными из скачанного JSON файла)
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=comeback-2a6b2
FIREBASE_PRIVATE_KEY_ID=ваш_private_key_id_из_json
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nВАШ_ПРИВАТНЫЙ_КЛЮЧ_ИЗ_JSON\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@comeback-2a6b2.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=ваш_client_id
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40comeback-2a6b2.iam.gserviceaccount.com

# Firebase Database URL (уже правильный)
FIREBASE_DATABASE_URL=https://comeback-2a6b2-default-rtdb.firebaseio.com/
```

### Шаг 3: Пример заполнения

Если ваш скачанный JSON файл выглядит так:
```json
{
  "type": "service_account",
  "project_id": "comeback-2a6b2",
  "private_key_id": "abcd1234efgh5678",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-abc123@comeback-2a6b2.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-abc123%40comeback-2a6b2.iam.gserviceaccount.com"
}
```

То в `.env` файле укажите:
```env
FIREBASE_PRIVATE_KEY_ID=abcd1234efgh5678
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-abc123@comeback-2a6b2.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=123456789012345678901
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-abc123%40comeback-2a6b2.iam.gserviceaccount.com
```

### Шаг 4: Перезапуск сервера

После заполнения .env файла:
1. Остановите Django сервер (Ctrl+C)
2. Запустите заново: `python manage.py runserver`
3. Статус Firebase изменится на "✅ Firebase подключен"

## 🎯 Что получите после настройки

- ✅ **Автоматическая синхронизация**: Все видео из Django попадают в Unity
- ✅ **Реальное время**: Unity получает обновления мгновенно  
- ✅ **Статистика платежей**: Синхронизация данных о платежах
- ✅ **Полная интеграция**: Django ↔ Firebase ↔ Unity

## 🚨 Важно!

1. **Приватный ключ** должен быть скопирован целиком включая `\n`
2. **Кавычки** вокруг private_key обязательны
3. **Не делитесь** этими ключами - они дают полный доступ к Firebase

## 🔧 Проверка работы

После настройки:
1. Войдите в Django админ панель
2. На главной странице увидите "✅ Firebase подключен"
3. Добавьте тестовое видео
4. Оно автоматически появится в Unity приложении

---

**Нужна помощь?** Покажите содержимое скачанного JSON файла (без приватного ключа) и я помогу заполнить .env файл правильно.
