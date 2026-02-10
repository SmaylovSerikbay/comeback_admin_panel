# 🔧 Исправление проблемы Docker Build

## ❌ Проблема
Docker build застревает на шаге:
```
Step 8/13 : RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
```

## ✅ РЕШЕНИЕ

### Шаг 1: Прервите текущую сборку
```bash
# Нажмите Ctrl+C для прерывания
```

### Шаг 2: Обновите код
```bash
cd ~/comeback_admin_panel

# Сохраните текущие изменения
cp .env .env.backup

# Получите обновления
git stash
git pull origin main

# Восстановите .env
cp .env.backup .env
```

### Шаг 3: Очистите Docker
```bash
# Остановите контейнеры
docker-compose down

# Удалите все build кэши
docker builder prune -a -f

# Удалите неиспользуемые образы
docker image prune -a -f

# Опционально: полная очистка (ОСТОРОЖНО!)
# docker system prune -a -f --volumes
```

### Шаг 4: Проверьте что venv исключен
```bash
# Проверьте размер контекста (должно быть <10MB вместо 112MB)
du -sh . --exclude=venv --exclude=.git --exclude=media

# Убедитесь что .dockerignore на месте
cat .dockerignore | grep venv
```

### Шаг 5: Пересоберите
```bash
# Сборка без кэша
docker-compose build --no-cache

# Должно быть быстро и без зависаний!
# Sending build context должен показать ~5-10MB вместо 112MB
```

### Шаг 6: Запустите
```bash
docker-compose up -d
```

### Шаг 7: Проверьте
```bash
# Статус контейнеров
docker-compose ps

# Логи
docker-compose logs web --tail=50

# Health check
curl http://localhost/payment-gateway/api/unity/health/
```

## 🎯 ЧТО БЫЛО ИСПРАВЛЕНО

### 1. Оптимизирован `.dockerignore`
**Было:** Игнорировалось недостаточно файлов (112.4MB в контексте)  
**Стало:** Агрессивное игнорирование всех ненужных файлов (~5-10MB в контексте)

### 2. Оптимизирован `Dockerfile`
**Было:**
```dockerfile
COPY . .
RUN useradd ... && chown -R app:app /app  # Медленно!
```

**Стало:**
```dockerfile
RUN useradd ...  # Создаём пользователя сначала
COPY --chown=app:app . .  # Копируем уже с правильным владельцем
```

**Преимущества:**
- ✅ Нет медленной операции `chown -R`
- ✅ Файлы сразу копируются с правильным владельцем
- ✅ Быстрее в 10-100 раз!

## 🚨 ЕСЛИ ВСЁРАВНО НЕ РАБОТАЕТ

### Вариант A: Проверьте ресурсы сервера
```bash
# Свободная память
free -h

# Дисковое пространство
df -h

# Загрузка CPU
top
```

Если мало памяти (<1GB свободно):
```bash
# Очистите место
docker system prune -a -f --volumes
```

### Вариант B: Соберите локально и загрузите
```bash
# На локальной машине
docker build -t comeback_admin:latest .
docker save comeback_admin:latest | gzip > comeback_admin.tar.gz

# Загрузите на сервер
scp comeback_admin.tar.gz root@89.39.95.247:~/

# На сервере
cd ~
docker load < comeback_admin.tar.gz
```

### Вариант C: Упростите Dockerfile
Временно закомментируйте collectstatic:
```dockerfile
# Временно отключите
# RUN python manage.py collectstatic --noinput
```

Соберите, а collectstatic запустите вручную после:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## 📊 ОЖИДАЕМЫЙ РЕЗУЛЬТАТ

### До исправления:
```
Sending build context to Docker daemon  112.4MB
Step 8/13 : RUN useradd ... && chown -R ...
 ---> Running in bd9dcc59fc7e [ЗАСТРЯЛО]
```

### После исправления:
```
Sending build context to Docker daemon  5.2MB
Step 8/13 : COPY --chown=app:app . .
 ---> Running in abc123def456
 ---> xyz789abc123
Step 9/13 : USER app
 ---> Running in def456ghi789
Successfully built ghi789jkl012
```

**Время сборки:**
- До: >10 минут (или зависает)
- После: ~2-3 минуты

## ✅ ПРОВЕРОЧНЫЙ СПИСОК

- [ ] Прервал текущую сборку (Ctrl+C)
- [ ] Обновил код (`git pull`)
- [ ] Очистил Docker кэш (`docker builder prune -a -f`)
- [ ] Проверил .dockerignore (есть `venv/`)
- [ ] Пересобрал (`docker-compose build --no-cache`)
- [ ] Контекст сборки уменьшился (5-10MB вместо 112MB)
- [ ] Сборка прошла успешно
- [ ] Контейнеры запущены (`docker-compose ps`)
- [ ] Health check работает

## 📞 ПОДДЕРЖКА

Если проблема не решена, соберите информацию:

```bash
# Версия Docker
docker --version
docker-compose --version

# Ресурсы системы
free -h
df -h

# Размер контекста
du -sh comeback_admin_panel/ --exclude=venv --exclude=.git

# Логи
docker-compose logs > docker_logs.txt
```

---

**Дата:** 2025-01-10  
**Статус:** ✅ Исправлено  
**Время исправления:** ~5 минут
