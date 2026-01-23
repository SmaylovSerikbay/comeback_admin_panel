#!/bin/bash

# Скрипт развертывания Comeback Admin Panel на VDS
# Использование: ./deploy.sh

set -e

echo "🚀 Начинаем развертывание Comeback Admin Panel на VDS..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Устанавливаем..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker установлен"
else
    echo "✅ Docker уже установлен"
fi

# Проверяем наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Устанавливаем..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose установлен"
else
    echo "✅ Docker Compose уже установлен"
fi

# Создаем необходимые директории
echo "📁 Создаем директории..."
mkdir -p nginx/ssl
mkdir -p nginx/www
mkdir -p media
mkdir -p staticfiles

# Устанавливаем права на директории
sudo chown -R $USER:$USER nginx/
sudo chown -R $USER:$USER media/
sudo chown -R $USER:$USER staticfiles/

# Останавливаем существующие контейнеры
echo "🛑 Останавливаем существующие контейнеры..."
docker-compose down -v 2>/dev/null || true

# Удаляем старые образы
echo "🧹 Очищаем старые образы..."
docker system prune -f

# Создаем .env файл из env.production
echo "📝 Создаем .env файл..."
cp env.production .env

# Запускаем сервисы
echo "🚀 Запускаем сервисы..."
docker-compose up -d --build

# Ждем запуска базы данных
echo "⏳ Ждем запуска базы данных..."
sleep 30

# Создаем суперпользователя
echo "👤 Создаем суперпользователя..."
docker-compose exec web python manage.py createsuperuser --noinput || true

# Проверяем статус сервисов
echo "📊 Проверяем статус сервисов..."
docker-compose ps

echo ""
echo "🎉 Развертывание завершено!"
echo ""
echo "📱 Ваше приложение доступно по адресам:"
echo "   HTTP:  http://89.39.95.247"
echo "   HTTPS: https://89.39.95.247"
echo ""
echo "🔧 Полезные команды:"
echo "   Просмотр логов: docker-compose logs -f"
echo "   Остановка: docker-compose down"
echo "   Перезапуск: docker-compose restart"
echo "   Обновление: docker-compose pull && docker-compose up -d"
echo ""
echo "⚠️  ВАЖНО: Не забудьте настроить Firebase credentials в .env файле!"
echo "⚠️  ВАЖНО: Измените SECRET_KEY в .env файле!"
echo ""
