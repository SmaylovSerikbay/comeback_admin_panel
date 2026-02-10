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

# Создаем пользователя ДО копирования файлов (оптимизация)
RUN useradd --create-home --shell /bin/bash app

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY --chown=app:app . .

# Переключаемся на пользователя app
USER app

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "comeback_admin.wsgi:application"]
