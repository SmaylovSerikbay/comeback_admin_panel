# 🚀 Развертывание Comeback Admin Panel на VDS

## 📋 Предварительные требования

- VDS с Ubuntu 20.04+ или CentOS 8+
- SSH доступ к серверу
- Домен или IP адрес (в нашем случае: 89.39.95.190)
- Минимум 2GB RAM, 20GB дискового пространства

## 🔧 Шаг 1: Подключение к VDS

```bash
ssh root@89.39.95.190
```

## 🐳 Шаг 2: Установка Docker и Docker Compose

### Ubuntu/Debian:
```bash
# Обновляем систему
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
apt install -y curl wget git unzip

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Добавляем пользователя в группу docker
usermod -aG docker $USER

# Устанавливаем Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Перезагружаемся
reboot
```

### CentOS/RHEL:
```bash
# Обновляем систему
yum update -y

# Устанавливаем необходимые пакеты
yum install -y curl wget git unzip

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Запускаем Docker
systemctl start docker
systemctl enable docker

# Устанавливаем Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

## 📁 Шаг 3: Клонирование проекта

```bash
# Клонируем репозиторий
git clone https://github.com/SmaylovSerikbay/comeback_admin_panel.git
cd comeback_admin_panel

# Создаем необходимые директории
mkdir -p nginx/ssl nginx/www media staticfiles
```

## ⚙️ Шаг 4: Настройка окружения

### 4.1 Создание .env файла
```bash
# Копируем production настройки
cp env.production .env

# Редактируем .env файл
nano .env
```

### 4.2 Настройка Firebase
1. Перейдите в [Firebase Console](https://console.firebase.google.com/)
2. Выберите проект `comeback-2a6b2`
3. Перейдите в Project Settings > Service Accounts
4. Создайте новый приватный ключ
5. Скопируйте данные в `.env` файл

### 4.3 Изменение SECRET_KEY
```bash
# Генерируем новый SECRET_KEY
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Копируем результат в .env файл
nano .env
```

## 🚀 Шаг 5: Запуск приложения

### 5.1 Первый запуск
```bash
# Собираем и запускаем контейнеры
docker-compose up -d --build

# Проверяем статус
docker-compose ps

# Смотрим логи
docker-compose logs -f
```

### 5.2 Создание суперпользователя
```bash
# Создаем суперпользователя Django
docker-compose exec web python manage.py createsuperuser

# Создаем роли пользователей
docker-compose exec web python manage.py shell
```

В Django shell:
```python
from django.contrib.auth.models import User
from video_manager.models import UserRole

# Создание администратора
admin_user = User.objects.get(username='your_admin_username')
UserRole.objects.create(user=admin_user, role='admin')

# Создание кассира
cashier_user = User.objects.create_user('cashier', 'cashier@example.com', 'password')
UserRole.objects.create(user=cashier_user, role='cashier')
```

## 🔒 Шаг 6: Настройка SSL (опционально)

### 6.1 Автоматический SSL с Let's Encrypt
```bash
# Запускаем certbot для получения SSL сертификата
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d 89.39.95.190

# Перезапускаем nginx
docker-compose restart nginx
```

### 6.2 Ручная настройка SSL
Если у вас есть собственный SSL сертификат:
```bash
# Копируем сертификаты в nginx/ssl/
cp your_certificate.crt nginx/ssl/
cp your_private_key.key nginx/ssl/

# Перезапускаем nginx
docker-compose restart nginx
```

## 📊 Шаг 7: Проверка работоспособности

### 7.1 Проверка сервисов
```bash
# Статус контейнеров
docker-compose ps

# Логи приложения
docker-compose logs web

# Логи nginx
docker-compose logs nginx

# Логи базы данных
docker-compose logs db
```

### 7.2 Проверка веб-интерфейса
- Откройте браузер
- Перейдите по адресу: `http://89.39.95.190` или `https://89.39.95.190`
- Войдите с созданными учетными данными

## 🔧 Шаг 8: Управление приложением

### 8.1 Основные команды
```bash
# Остановка
docker-compose down

# Запуск
docker-compose up -d

# Перезапуск
docker-compose restart

# Обновление
docker-compose pull
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f [service_name]

# Вход в контейнер
docker-compose exec web bash
docker-compose exec db psql -U comeback_user -d comeback_admin
```

### 8.2 Резервное копирование
```bash
# Резервное копирование базы данных
docker-compose exec db pg_dump -U comeback_user comeback_admin > backup_$(date +%Y%m%d_%H%M%S).sql

# Резервное копирование медиа файлов
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### 8.3 Восстановление
```bash
# Восстановление базы данных
docker-compose exec -T db psql -U comeback_user comeback_admin < backup_file.sql

# Восстановление медиа файлов
tar -xzf media_backup_file.tar.gz
```

## 🚨 Устранение проблем

### Проблема: Контейнеры не запускаются
```bash
# Проверяем логи
docker-compose logs

# Проверяем использование портов
netstat -tlnp | grep :80
netstat -tlnp | grep :443

# Очищаем Docker
docker system prune -f
docker volume prune -f
```

### Проблема: База данных не подключается
```bash
# Проверяем статус PostgreSQL
docker-compose exec db pg_isready -U comeback_user

# Проверяем логи базы данных
docker-compose logs db
```

### Проблема: Nginx не работает
```bash
# Проверяем конфигурацию
docker-compose exec nginx nginx -t

# Перезапускаем nginx
docker-compose restart nginx
```

## 📈 Мониторинг и логи

### 8.1 Просмотр логов в реальном времени
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db
```

### 8.2 Мониторинг ресурсов
```bash
# Использование ресурсов контейнерами
docker stats

# Использование дискового пространства
df -h
docker system df
```

## 🔄 Обновление приложения

### 8.1 Обновление кода
```bash
# Останавливаем приложение
docker-compose down

# Получаем обновления
git pull origin main

# Пересобираем и запускаем
docker-compose up -d --build
```

### 8.2 Обновление зависимостей
```bash
# Обновляем requirements.txt
docker-compose exec web pip install --upgrade -r requirements.txt

# Перезапускаем приложение
docker-compose restart web
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs -f`
2. Убедитесь, что все порты свободны
3. Проверьте настройки в `.env` файле
4. Убедитесь в правильности Firebase конфигурации

## 🎯 Следующие шаги

После успешного развертывания:

1. Настройте регулярные резервные копии
2. Настройте мониторинг сервера
3. Настройте автоматическое обновление SSL сертификатов
4. Настройте firewall и дополнительные меры безопасности

---

**Успешного развертывания! 🎉**
