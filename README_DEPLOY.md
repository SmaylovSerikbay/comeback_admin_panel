# 🚀 Развертывание Comeback Admin Panel на VDS

## 📋 Краткое описание

Этот проект представляет собой Django-приложение для управления AR-контентом с интеграцией Firebase. Проект готов к развертыванию на VDS с использованием Docker.

## 🎯 Что получится

- **Django приложение** с PostgreSQL базой данных
- **Nginx веб-сервер** с SSL поддержкой
- **Redis кэш** для улучшения производительности
- **Автоматическое SSL** с Let's Encrypt
- **Мониторинг и логирование**
- **Безопасность** с настроенным firewall

## 🔧 Быстрое развертывание

### Шаг 1: Подключение к VDS
```bash
ssh root@89.39.95.247
```

### Шаг 2: Автоматическое развертывание
```bash
# Клонируем проект
git clone https://github.com/SmaylovSerikbay/comeback_admin_panel.git
cd comeback_admin_panel

# Делаем скрипт исполняемым
chmod +x quick_deploy.sh

# Запускаем автоматическое развертывание
./quick_deploy.sh
```

## 📁 Структура проекта

```
comeback_admin_panel/
├── Dockerfile                 # Docker образ для Django
├── docker-compose.yml        # Docker Compose конфигурация
├── requirements.txt          # Python зависимости
├── quick_deploy.sh          # Автоматическое развертывание
├── setup_firewall.sh        # Настройка firewall
├── monitor.sh               # Мониторинг приложения
├── env.production           # Production настройки
├── nginx/                   # Nginx конфигурация
│   └── nginx.conf
├── comeback_admin/          # Django проект
├── video_manager/           # Приложение управления видео
├── sales_dashboard/         # Дашборд продаж
├── subscription/            # Управление подписками
├── otp_manager/            # Управление OTP
└── cashier/                # Приложение кассира
```

## 🐳 Docker сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| **web** | 8000 | Django приложение |
| **nginx** | 80/443 | Веб-сервер с SSL |
| **db** | 5432 | PostgreSQL база данных |
| **redis** | 6379 | Redis кэш |
| **certbot** | - | SSL сертификаты |

## ⚙️ Настройка окружения

### 1. Firebase настройки
Отредактируйте `.env` файл:
```bash
nano .env
```

Настройте Firebase credentials:
```env
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=comeback-2a6b2
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_CERT_URL=your_client_cert_url
```

### 2. Генерация SECRET_KEY
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🚀 Управление приложением

### Основные команды
```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f

# Статус сервисов
docker-compose ps
```

### Создание пользователей
```bash
# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Создание ролей
docker-compose exec web python manage.py shell
```

В Django shell:
```python
from django.contrib.auth.models import User
from video_manager.models import UserRole

# Администратор
admin_user = User.objects.get(username='admin')
UserRole.objects.create(user=admin_user, role='admin')

# Кассир
cashier_user = User.objects.create_user('cashier', 'cashier@example.com', 'password')
UserRole.objects.create(user=cashier_user, role='cashier')
```

## 🔒 Безопасность

### Настройка firewall
```bash
chmod +x setup_firewall.sh
./setup_firewall.sh
```

### SSL сертификаты
```bash
# Автоматический SSL
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d admin.comeback.uz

# Перезапуск nginx
docker-compose restart nginx
```

## 📊 Мониторинг

### Проверка статуса
```bash
chmod +x monitor.sh
./monitor.sh
```

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db
```

### Мониторинг ресурсов
```bash
# Использование ресурсов
docker stats

# Дисковое пространство
docker system df
```

## 🔄 Обновление

### Обновление кода
```bash
# Остановка
docker-compose down

# Получение обновлений
git pull origin main

# Пересборка и запуск
docker-compose up -d --build
```

### Обновление зависимостей
```bash
# Обновление requirements.txt
docker-compose exec web pip install --upgrade -r requirements.txt

# Перезапуск
docker-compose restart web
```

## 🚨 Устранение проблем

### Контейнеры не запускаются
```bash
# Проверка логов
docker-compose logs

# Очистка Docker
docker system prune -f
docker volume prune -f
```

### База данных не подключается
```bash
# Проверка статуса
docker-compose exec db pg_isready -U comeback_user

# Проверка логов
docker-compose logs db
```

### Nginx не работает
```bash
# Проверка конфигурации
docker-compose exec nginx nginx -t

# Перезапуск
docker-compose restart nginx
```

## 📈 Резервное копирование

### База данных
```bash
# Создание бэкапа
docker-compose exec db pg_dump -U comeback_user comeback_admin > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление
docker-compose exec -T db psql -U comeback_user comeback_admin < backup_file.sql
```

### Медиа файлы
```bash
# Создание бэкапа
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/

# Восстановление
tar -xzf media_backup_file.tar.gz
```

## 🌐 Доступ к приложению

После успешного развертывания:

- **HTTP**: http://89.39.95.247
- **HTTPS**: https://admin.comeback.uz
- **Admin**: https://admin.comeback.uz/admin/

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs -f`
2. Запустите мониторинг: `./monitor.sh`
3. Проверьте настройки в `.env` файле
4. Убедитесь в правильности Firebase конфигурации

## 🎯 Следующие шаги

После успешного развертывания:

1. ✅ Настройте регулярные резервные копии
2. ✅ Настройте мониторинг сервера
3. ✅ Настройте автоматическое обновление SSL
4. ✅ Настройте дополнительные меры безопасности

---

## 🎉 Готово!

Ваше приложение **Comeback Admin Panel** успешно развернуто на VDS!

**IP адрес**: 89.39.95.247  
**Статус**: 🟢 Работает  
**Версия**: 1.0  
**Последнее обновление**: 2025-01-08

---

**Успешного использования! 🚀**
