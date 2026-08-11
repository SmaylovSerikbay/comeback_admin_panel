#!/bin/bash

# Скрипт мониторинга Comeback Admin Panel
# Показывает статус всех сервисов и ресурсов

echo "📊 Мониторинг Comeback Admin Panel"
echo "=================================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для проверки статуса
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Проверяем статус Docker
echo -e "${BLUE}🐳 Docker Status:${NC}"
if command -v docker &> /dev/null; then
    if systemctl is-active --quiet docker; then
        echo -e "${GREEN}✅ Docker запущен${NC}"
    else
        echo -e "${RED}❌ Docker не запущен${NC}"
    fi
else
    echo -e "${RED}❌ Docker не установлен${NC}"
fi

# Проверяем статус Docker Compose
echo -e "${BLUE}📦 Docker Compose Status:${NC}"
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✅ Docker Compose установлен${NC}"
else
    echo -e "${RED}❌ Docker Compose не установлен${NC}"
fi

echo ""

# Проверяем статус контейнеров
echo -e "${BLUE}🚀 Container Status:${NC}"
if [ -f "docker-compose.yml" ]; then
    if docker-compose ps | grep -q "Up"; then
        echo -e "${GREEN}✅ Контейнеры запущены${NC}"
        docker-compose ps
    else
        echo -e "${RED}❌ Контейнеры не запущены${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  docker-compose.yml не найден${NC}"
fi

echo ""

# Проверяем использование ресурсов
echo -e "${BLUE}💾 Resource Usage:${NC}"
echo "Disk Usage:"
df -h | grep -E '^/dev/'

echo ""
echo "Memory Usage:"
free -h

echo ""
echo "Docker Disk Usage:"
docker system df

echo ""

# Проверяем доступность приложения
echo -e "${BLUE}🌐 Application Status:${NC}"
if curl -s http://localhost > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Приложение доступно по HTTP${NC}"
else
    echo -e "${RED}❌ Приложение недоступно по HTTP${NC}"
fi

if curl -s https://localhost > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Приложение доступно по HTTPS${NC}"
else
    echo -e "${YELLOW}⚠️  Приложение недоступно по HTTPS${NC}"
fi

echo ""

# Проверяем логи на ошибки
echo -e "${BLUE}📝 Recent Errors (last 10 lines):${NC}"
if [ -f "docker-compose.yml" ]; then
    docker-compose logs --tail=10 | grep -i error || echo "Ошибок не найдено"
else
    echo "docker-compose.yml не найден"
fi

echo ""

# Проверяем порты
echo -e "${BLUE}🔌 Port Status:${NC}"
echo "Listening ports:"
netstat -tlnp | grep -E ':(80|443|8000|5432|6379)' || echo "Нет активных портов"

echo ""

# Проверяем firewall
echo -e "${BLUE}🔥 Firewall Status:${NC}"
if command -v ufw &> /dev/null; then
    ufw status | head -5
else
    echo "UFW не установлен"
fi

echo ""

# Показываем последние логи
echo -e "${BLUE}📋 Recent Logs (last 5 lines):${NC}"
if [ -f "docker-compose.yml" ]; then
    docker-compose logs --tail=5
else
    echo "docker-compose.yml не найден"
fi

echo ""
echo "🔧 Полезные команды:"
echo "   Подробные логи: docker-compose logs -f"
echo "   Перезапуск: docker-compose restart"
echo "   Остановка: docker-compose down"
echo "   Статус: docker-compose ps"
echo "   Мониторинг ресурсов: docker stats"
echo ""
