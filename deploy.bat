@echo off
chcp 65001 >nul
echo 🚀 Начинаем развертывание Comeback Admin Panel на VDS...

REM Создаем необходимые директории
echo 📁 Создаем директории...
if not exist "nginx\ssl" mkdir nginx\ssl
if not exist "nginx\www" mkdir nginx\www
if not exist "media" mkdir media
if not exist "staticfiles" mkdir staticfiles

REM Создаем .env файл из env.production
echo 📝 Создаем .env файл...
copy env.production .env

REM Запускаем сервисы
echo 🚀 Запускаем сервисы...
docker-compose up -d --build

REM Ждем запуска базы данных
echo ⏳ Ждем запуска базы данных...
timeout /t 30 /nobreak >nul

REM Создаем суперпользователя
echo 👤 Создаем суперпользователя...
docker-compose exec web python manage.py createsuperuser --noinput

REM Проверяем статус сервисов
echo 📊 Проверяем статус сервисов...
docker-compose ps

echo.
echo 🎉 Развертывание завершено!
echo.
echo 📱 Ваше приложение доступно по адресам:
echo    HTTP:  http://89.39.95.247
echo    HTTPS: https://89.39.95.247
echo.
echo 🔧 Полезные команды:
echo    Просмотр логов: docker-compose logs -f
echo    Остановка: docker-compose down
echo    Перезапуск: docker-compose restart
echo    Обновление: docker-compose pull ^&^& docker-compose up -d
echo.
echo ⚠️  ВАЖНО: Не забудьте настроить Firebase credentials в .env файле!
echo ⚠️  ВАЖНО: Измените SECRET_KEY в .env файле!
echo.
pause
