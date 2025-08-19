#!/bin/bash

# Быстрый скрипт развертывания Comeback Admin Panel на VDS
# Автоматически выполняет все необходимые шаги

set -e

echo "🚀 Быстрое развертывание Comeback Admin Panel на VDS..."
echo "IP: 89.39.95.190"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для логирования
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Проверяем, что мы root
if [[ $EUID -ne 0 ]]; then
   error "Этот скрипт должен быть запущен от root пользователя"
fi

# Проверяем наличие curl
if ! command -v curl &> /dev/null; then
    log "Устанавливаем curl..."
    apt update -y
    apt install -y curl wget git unzip
fi

# Устанавливаем Docker
if ! command -v docker &> /dev/null; then
    log "Устанавливаем Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    
    # Запускаем Docker
    systemctl start docker
    systemctl enable docker
    
    log "Docker установлен и запущен"
else
    log "Docker уже установлен"
fi

# Устанавливаем Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log "Устанавливаем Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    log "Docker Compose установлен"
else
    log "Docker Compose уже установлен"
fi

# Клонируем проект
if [ ! -d "comeback_admin_panel" ]; then
    log "Клонируем проект..."
    git clone https://github.com/SmaylovSerikbay/comeback_admin_panel.git
    cd comeback_admin_panel
else
    log "Проект уже клонирован, переходим в директорию..."
    cd comeback_admin_panel
fi

# Создаем необходимые директории
log "Создаем директории..."
mkdir -p nginx/ssl nginx/www media staticfiles

# Устанавливаем права
chown -R $USER:$USER nginx/ media/ staticfiles/

# Создаем .env файл
if [ ! -f ".env" ]; then
    log "Создаем .env файл..."
    if [ -f "env.production" ]; then
        cp env.production .env
        warning "Файл .env создан из env.production. Не забудьте настроить Firebase credentials!"
    else
        # Создаем базовый .env файл
        cat > .env << EOF
# Django Settings
DEBUG=False
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
ALLOWED_HOSTS=89.39.95.190,localhost,127.0.0.1

# Database
POSTGRES_DB=comeback_admin
POSTGRES_USER=comeback_user
POSTGRES_PASSWORD=comeback_password_2025
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECURE_SSL_REDIRECT=True

# Firebase Configuration - НАСТРОЙТЕ ЭТИ ЗНАЧЕНИЯ!
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=comeback-2a6b2
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_CERT_URL=your_client_cert_url
FIREBASE_DATABASE_URL=https://comeback-2a6b2-default-rtdb.firebaseio.com/
FIREBASE_STORAGE_BUCKET=comeback-2a6b2.firebasestorage.app
EOF
        warning "Создан базовый .env файл. ОБЯЗАТЕЛЬНО настройте Firebase credentials!"
    fi
else
    log ".env файл уже существует"
fi

# Останавливаем существующие контейнеры
log "Останавливаем существующие контейнеры..."
docker-compose down -v 2>/dev/null || true

# Очищаем Docker
log "Очищаем Docker..."
docker system prune -f

# Запускаем сервисы
log "Запускаем сервисы..."
docker-compose up -d --build

# Ждем запуска базы данных
log "Ждем запуска базы данных..."
sleep 45

# Проверяем статус сервисов
log "Проверяем статус сервисов..."
docker-compose ps

# Создаем суперпользователя
log "Создаем суперпользователя..."
docker-compose exec -T web python manage.py createsuperuser --noinput || warning "Не удалось создать суперпользователя (возможно уже существует)"

# Проверяем доступность приложения
log "Проверяем доступность приложения..."
sleep 10

if curl -s http://localhost > /dev/null; then
    log "✅ Приложение успешно запущено!"
else
    warning "Приложение может быть еще не готово, проверьте логи: docker-compose logs -f"
fi

echo ""
echo "🎉 Развертывание завершено!"
echo ""
echo "📱 Ваше приложение доступно по адресам:"
echo "   HTTP:  http://89.39.95.190"
echo "   HTTPS: https://89.39.95.190"
echo ""
echo "🔧 Полезные команды:"
echo "   Просмотр логов: docker-compose logs -f"
echo "   Остановка: docker-compose down"
echo "   Перезапуск: docker-compose restart"
echo "   Статус: docker-compose ps"
echo ""
echo "⚠️  ВАЖНЫЕ НАПОМИНАНИЯ:"
echo "   1. Настройте Firebase credentials в .env файле"
echo "   2. Измените пароли в .env файле"
echo "   3. Настройте SSL сертификаты"
echo ""
echo "📚 Подробная документация: DEPLOYMENT.md"
echo ""
