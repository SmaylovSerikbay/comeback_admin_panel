#!/bin/bash

# Альтернативная установка Docker для Ubuntu 16.04
set -e

echo "🐳 Альтернативная установка Docker для Ubuntu 16.04..."

# Обновляем пакеты
apt-get update -y

# Устанавливаем Docker из репозитория Ubuntu (старая версия, но работает)
apt-get install -y docker.io

# Запускаем Docker
systemctl start docker
systemctl enable docker

# Проверяем
docker --version

echo "✅ Docker установлен!"
