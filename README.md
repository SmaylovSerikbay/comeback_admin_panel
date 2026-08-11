# ComeBack Admin Panel

Django веб-панель для управления AR приложением ComeBack с интеграцией Firebase и системой ролей.

## 🚨 ВАЖНО: Решение проблемы Unity Payment Gateway

**Если вы получаете ошибку Unity:** `Endpoint unavailable - check server settings`

➡️ **Откройте файл `РЕШЕНИЕ_ПРОБЛЕМЫ_UNITY.md`** для быстрого решения (5 минут)

Или используйте:
- **QUICK_FIX.md** - мгновенное исправление
- **DEPLOYMENT_STEPS.md** - пошаговая инструкция
- **UNITY_INTEGRATION.md** - полная документация Unity

## 🖥 Админка на Next.js (новая)

В папке **`admin-next/`** — вариант админ-панели на Next.js 14 с тем же функционалом и современным UI (Tailwind). Запуск: см. **`admin-next/README.md`**. Бэкенд — тот же Django; добавлен REST API под токен-авторизацию (`/api/`).

## 🚀 Возможности

### Роли пользователей:
- **Администратор**: Полный доступ ко всем функциям
- **Кассир**: Просмотр платежей и базовой статистики

### Функциональность администратора:
- ✅ Добавление видео с GPS координатами
- ✅ Управление AR контентом
- ✅ Синхронизация с Firebase Realtime Database
- ✅ Просмотр детальной статистики продаж
- ✅ Управление пользователями

### Функциональность кассира:
- ✅ Просмотр списка платежей
- ✅ Базовая статистика продаж
- ✅ Фильтрация по статусам и датам

## 🛠 Установка

### 1. Клонирование и настройка

```bash
# Переход в папку проекта
cd comeback_admin_panel

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
# Скопируйте файл конфигурации
copy env_example.txt .env

# Отредактируйте .env файл с вашими настройками
```

### 3. Настройка Firebase

1. Перейдите в [Firebase Console](https://console.firebase.google.com/)
2. Выберите проект `comeback-2a6b2`
3. Перейдите в Project Settings > Service Accounts
4. Создайте новый приватный ключ
5. Скопируйте данные в `.env` файл

### 4. Инициализация базы данных

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
```

### 5. Настройка ролей пользователей

```bash
# Запуск Django shell
python manage.py shell
```

```python
# В Django shell:
from django.contrib.auth.models import User
from video_manager.models import UserRole

# Создание администратора
admin_user = User.objects.get(username='your_admin_username')
UserRole.objects.create(user=admin_user, role='admin')

# Создание кассира
cashier_user = User.objects.create_user('cashier', 'cashier@example.com', 'password')
UserRole.objects.create(user=cashier_user, role='cashier')
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

Откройте браузер и перейдите по адресу: http://127.0.0.1:8000

## 📱 Использование

### Добавление видео

1. Войдите как администратор
2. Перейдите в раздел "Видео" → "Добавить видео"
3. Получите GPS координаты:
   - Откройте [LatLong.net](https://www.latlong.net/)
   - Найдите нужное место
   - Скопируйте Latitude и Longitude
4. Загрузите видео файл или укажите URL
5. Сохраните - видео автоматически появится в Unity приложении

### Просмотр статистики

1. Главная страница - общая статистика
2. Раздел "Статистика" - детальная аналитика (только для админа)
3. Раздел "Платежи" - список всех транзакций

### Синхронизация с Firebase

- Все видео автоматически синхронизируются с Firebase
- Кнопка "Синхронизация Firebase" для принудительного обновления
- Статус подключения отображается на главной странице

## 🔧 Конфигурация

### Firebase настройки

Файл: `firebase_service.py`
- Подключение к Firebase Realtime Database
- Автоматическая синхронизация видео объектов
- Получение статистики платежей

### Структура данных Firebase

```json
{
  "objects": {
    "video_id": {
      "id": "uuid",
      "x": "latitude",
      "y": "longitude", 
      "objectType": "video",
      "objectURL": "video_url",
      "title": "video_title",
      "description": "video_description",
      "created_at": "timestamp",
      "created_by": "username",
      "is_active": true
    }
  },
  "payments": {
    "order_id": {
      "amount": 1000,
      "currency": "UZS",
      "status": "success",
      "created_at": "timestamp"
    }
  }
}
```

## 🎯 Интеграция с Unity

### Как это работает:

1. **Добавление видео** в админ панели
2. **Автоматическая отправка** в Firebase Realtime Database  
3. **Unity приложение** получает обновления в реальном времени
4. **VideoSpawner.cs** загружает новые видео объекты
5. **AR система** размещает видео по GPS координатам

### Формат данных для Unity:

```csharp
// В Unity VideoSpawner.cs ожидает:
{
    "id": "unique_id",
    "x": latitude,      // Широта
    "y": longitude,     // Долгота  
    "objectType": "video",
    "objectURL": "video_url"
}
```

## 📊 API Endpoints

### Основные URL:

- `/` - Главная страница (перенаправление на дашборд)
- `/login/` - Страница входа
- `/dashboard/` - Главный дашборд
- `/videos/` - Управление видео (только админ)
- `/videos/instructions/` - Инструкции по добавлению
- `/admin/` - Django админ панель

## 🔐 Безопасность

### Рекомендации:

1. **Измените SECRET_KEY** в production
2. **Настройте ALLOWED_HOSTS** для production
3. **Используйте HTTPS** в production
4. **Ограничьте доступ** к Firebase ключам
5. **Регулярно обновляйте** зависимости

### Роли и права:

- **Суперпользователь**: Полный доступ через Django Admin
- **Администратор**: Управление видео + статистика
- **Кассир**: Только просмотр платежей

## 🐛 Устранение проблем

### Частые ошибки:

1. **Firebase connection error**:
   - Проверьте правильность ключей в `.env`
   - Убедитесь что проект активен в Firebase

2. **Video upload fails**:
   - Проверьте размер файла (макс. 50MB)
   - Убедитесь что папка `media/` доступна для записи

3. **Coordinates not working**:
   - Используйте точки вместо запятых в координатах
   - Проверьте диапазон: Latitude (-90, 90), Longitude (-180, 180)

### Логи и отладка:

```bash
# Просмотр логов Django
python manage.py runserver --verbosity=2

# Проверка Firebase подключения
python manage.py shell
>>> from firebase_service import firebase_service
>>> firebase_service.get_all_video_objects()
```

## 📈 Развитие

### Планы на будущее:

- [ ] Групповая загрузка видео
- [ ] Интеграция с YouTube API  
- [ ] Расширенная аналитика
- [ ] Мобильное приложение для управления
- [ ] Поддержка 3D моделей
- [ ] Система уведомлений

## 📞 Поддержка

При возникновении проблем:

1. Проверьте документацию выше
2. Изучите логи в консоли Django
3. Проверьте статус Firebase подключения
4. Убедитесь в правильности GPS координат с [LatLong.net](https://www.latlong.net/)

---

**Версия**: 1.0  
**Дата**: 2025-01-08  
**Совместимость**: Django 4.2+, Python 3.8+
