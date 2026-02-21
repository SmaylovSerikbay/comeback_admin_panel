# Используем официальный Python образ
FROM python:3.11-slim-bullseye

# Debian slim images sometimes include an APT post-invoke hook that can fail
# on some hosts/filesystems; disable it to make builds reliable.
RUN rm -f /etc/apt/apt.conf.d/docker-clean || true

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем entrypoint в корень образа (не в /app), чтобы том .:/app его не перезаписывал
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

# Копируем код приложения
COPY . .

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
