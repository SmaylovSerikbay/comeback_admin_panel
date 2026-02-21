# ComeBack Admin — Next.js

Красивая админ-панель на Next.js 14 с тем же функционалом, что и Django-шаблоны.

## Запуск через Docker (рекомендуется)

Из корня проекта (`comeback_admin_panel`):

```bash
docker compose up -d --build
```

- **Django (старая админка):** по адресу на порту 80 (или через nginx).
- **Next.js админка:** http://localhost:3000 — логин те же, что в Django.

Сервис Next собирается с прокси к API Django (`web:8000`), отдельно ничего поднимать не нужно.

## Запуск без Docker

### 1. Бэкенд (Django)

```bash
cd comeback_admin_panel
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Создайте токен для пользователя (при первом входе через API токен создастся сам, но можно и вручную):

```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> from rest_framework.authtoken.models import Token
>>> User = get_user_model()
>>> u = User.objects.get(username='admin')
>>> Token.objects.get_or_create(user=u)
```

### 2. Фронт (Next.js)

```bash
cd admin-next
npm install
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000). Логин — как в Django (логин/пароль пользователя).

### 3. Прокси к API

В разработке Next использует rewrites в `next.config.mjs`: запросы к `/api-backend/*` уходят на `http://127.0.0.1:8000/api/*`. Django должен быть запущен на порту 8000.

Если Django на другом хосте, задайте переменную окружения:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

Тогда клиент будет ходить напрямую на этот URL (нужно настроить CORS в Django для `http://localhost:3000`).

## Функционал

- **Дашборд** — сводка по платежам и выручке, последние платежи
- **Видео** — список, добавление (загрузка в Firebase Storage), редактирование, удаление (только админ)
- **Платежи** — список с фильтрами по статусу, дате и типу (онлайн / OTP)
- **OTP коды** — список, наличный платёж (создание одного или нескольких кодов), детали кода
- **Подписка** — настройки цены, длительности, валюты (только админ)
- **Статистика** — выручка по дням, по статусам, топ пользователей (только админ)

Роли (админ / кассир) те же, что в Django (модель `UserRole`).

## Стек

- Next.js 14 (App Router), TypeScript, Tailwind CSS
- Авторизация по токену (Django REST `TokenAuthentication`)
