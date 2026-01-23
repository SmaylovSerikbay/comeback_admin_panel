#!/bin/bash

# Установка Docker для Ubuntu 16.04
set -e

echo "🐳 Устанавливаем Docker для Ubuntu 16.04..."

# Обновляем пакеты
apt-get update -y

# Устанавливаем зависимости
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Добавляем GPG ключ Docker (старый метод для Ubuntu 16.04)
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Добавляем репозиторий Docker для Ubuntu 16.04 (xenial)
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Обновляем список пакетов
apt-get update -y

# Устанавливаем Docker (старая версия, совместимая с Ubuntu 16.04)
apt-get install -y docker-ce=17.12.1~ce-0~ubuntu || \
apt-get install -y docker-ce=18.06.3~ce~3-0~ubuntu || \
apt-get install -y docker-ce

# Запускаем Docker
systemctl start docker
systemctl enable docker

# Проверяем установку
docker --version

echo "✅ Docker установлен!"
