#!/bin/bash

# Скрипт настройки firewall для Comeback Admin Panel
# Настраивает UFW для безопасности VDS

set -e

echo "🔒 Настройка firewall для Comeback Admin Panel..."

# Проверяем, что мы root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Этот скрипт должен быть запущен от root пользователя"
   exit 1
fi

# Устанавливаем UFW если не установлен
if ! command -v ufw &> /dev/null; then
    echo "📦 Устанавливаем UFW..."
    apt update -y
    apt install -y ufw
fi

# Сбрасываем правила
echo "🔄 Сбрасываем правила firewall..."
ufw --force reset

# Устанавливаем политики по умолчанию
echo "⚙️ Устанавливаем политики по умолчанию..."
ufw default deny incoming
ufw default allow outgoing

# Разрешаем SSH (порт 22)
echo "🔑 Разрешаем SSH (порт 22)..."
ufw allow 22/tcp

# Разрешаем HTTP (порт 80)
echo "🌐 Разрешаем HTTP (порт 80)..."
ufw allow 80/tcp

# Разрешаем HTTPS (порт 443)
echo "🔒 Разрешаем HTTPS (порт 443)..."
ufw allow 443/tcp

# Разрешаем локальные подключения
echo "🏠 Разрешаем локальные подключения..."
ufw allow from 127.0.0.1
ufw allow from ::1

# Дополнительные порты для разработки (опционально)
# По умолчанию: НЕ открываем. Чтобы открыть, запустите так:
#   ALLOW_DEV_PORTS=y ./setup_firewall.sh
ALLOW_DEV_PORTS="${ALLOW_DEV_PORTS:-n}"
if [[ "${ALLOW_DEV_PORTS}" =~ ^[Yy]$ ]]; then
    echo "🔧 Разрешаем дополнительные порты для разработки..."
    ufw allow 8000/tcp  # Django development
    ufw allow 5432/tcp  # PostgreSQL
    ufw allow 6379/tcp  # Redis
else
    echo "✅ Дополнительные dev-порты не открываем (ALLOW_DEV_PORTS=${ALLOW_DEV_PORTS})"
fi

# Включаем firewall
echo "🚀 Включаем firewall..."
ufw --force enable

# Показываем статус
echo "📊 Статус firewall:"
ufw status verbose

echo ""
echo "✅ Firewall настроен и включен!"
echo ""
echo "🔧 Полезные команды:"
echo "   Статус: ufw status"
echo "   Правила: ufw status numbered"
echo "   Отключить: ufw disable"
echo "   Включить: ufw enable"
echo ""
echo "⚠️  ВАЖНО: Убедитесь, что SSH доступен перед закрытием сессии!"
echo ""
