# Получение SSL-сертификата вручную (Let's Encrypt) для admin.comeback.uz и comeback.uz

## Кратко (ручное получение)

1. **DNS**:
   - запись A для `admin.comeback.uz` → IP сервера (89.39.95.247)
   - запись A для `comeback.uz` и `www.comeback.uz` → тот же IP сервера (89.39.95.247)
   - порт 80 открыт.
2. **Сертификат** (на сервере, в каталоге проекта):
   ```bash
   cd ~/comeback_admin_panel
   mkdir -p nginx/www
   docker compose run --rm certbot certonly --webroot \
     --webroot-path=/var/www/certbot \
     --email admin@comeback.uz \
     --agree-tos --no-eff-email \
     -d admin.comeback.uz -d comeback.uz -d www.comeback.uz
   ```
   Файлы появятся в `./nginx/ssl/live/admin.comeback.uz/` и `./nginx/ssl/live/comeback.uz/` (fullchain.pem, privkey.pem).
3. **Включить HTTPS**: скопировать пример конфига и подключить его:
   ```bash
   cp nginx/conf.d/https.conf.example nginx/conf.d/https.conf
   ```
   В `nginx/nginx.conf` в конце блока `http { }` раскомментировать строку:
   ```nginx
   include /etc/nginx/conf.d/https.conf;
   ```
4. **Проверить и перезагрузить nginx**:
   ```bash
   docker compose exec nginx nginx -t && docker compose exec nginx nginx -s reload
   ```
5. В Django/settings и CORS при необходимости добавить `https://admin.comeback.uz`.

---

## 1. Подготовка на сервере

- Убедитесь, что **DNS** для `admin.comeback.uz` указывает на IP сервера (89.39.95.247).
- Порт **80** должен быть открыт (для проверки домена Let's Encrypt).
- Nginx и контейнеры уже запущены (`docker compose up -d`).

## 2. Получить сертификат через Certbot (на хосте, не в Docker)

Установите certbot, если его нет:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y certbot

# Или только certbot без установки (snap)
sudo snap install --classic certbot && sudo ln -sf /snap/bin/certbot /usr/bin/certbot
```

Временно отдайте порт 80 certbot (nginx не должен занимать 80 на время выдачи сертификата):

```bash
cd ~/comeback_admin_panel
docker compose stop nginx
```

Получите сертификат (webroot — файлы в папку, которую потом смонтирует nginx):

```bash
sudo mkdir -p ./nginx/www/.well-known/acme-challenge
sudo certbot certonly --webroot \
  --webroot-path="$(pwd)/nginx/www" \
  --email admin@comeback.uz \
  --agree-tos --no-eff-email \
  -d admin.comeback.uz
```

Certbot создаст файлы в `/etc/letsencrypt/live/admin.comeback.uz/` по умолчанию. Нужно **скопировать их в проект**, чтобы Docker их видел:

```bash
sudo mkdir -p ./nginx/ssl/live/admin.comeback.uz
sudo cp -L /etc/letsencrypt/live/admin.comeback.uz/fullchain.pem   ./nginx/ssl/live/admin.comeback.uz/
sudo cp -L /etc/letsencrypt/live/admin.comeback.uz/privkey.pem     ./nginx/ssl/live/admin.comeback.uz/
sudo chown -R "$USER:$USER" ./nginx/ssl
```

Запустите nginx снова:

```bash
docker compose start nginx
```

## 3. Вариант: Certbot в Docker (порт 80 у nginx)

Если не хотите останавливать nginx, используйте уже настроенный контейнер certbot. Сначала убедитесь, что в nginx есть location для ACME:

```text
location /.well-known/acme-challenge/ {
    root /var/www/certbot;
}
```

Папка на хосте: `./nginx/www` → в контейнере `/var/www/certbot`. Затем:

```bash
docker compose run --rm certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  --email admin@comeback.uz \
  --agree-tos --no-eff-email \
  -d admin.comeback.uz
```

Сертификаты появятся в `./nginx/ssl/live/admin.comeback.uz/` (том certbot смонтирован в `./nginx/ssl`).

## 4. Включить HTTPS в nginx

После того как в папке есть:

- `nginx/ssl/live/admin.comeback.uz/fullchain.pem`
- `nginx/ssl/live/admin.comeback.uz/privkey.pem`

Создайте конфиг HTTPS, например `nginx/conf.d/https.conf` (можно скопировать из `nginx/conf.d/https.conf.example`), и раскомментируйте в **конце** `nginx/nginx.conf` (внутри блока `http { }`):

```nginx
include /etc/nginx/conf.d/https.conf;
```

Перезагрузите nginx:

```bash
docker compose exec nginx nginx -t && docker compose exec nginx nginx -s reload
```

## 5. Обновление сертификата (раз в ~90 дней)

Проверка обновления вручную:

```bash
sudo certbot renew --dry-run
```

Обновить по факту:

```bash
sudo certbot renew
```

После обновления скопировать новые файлы в `./nginx/ssl/...` (как в шаге 2) и выполнить `docker compose exec nginx nginx -s reload`.

Можно настроить cron (на хосте):

```bash
0 3 * * * certbot renew --quiet && cp -L /etc/letsencrypt/live/admin.comeback.uz/*.pem /path/to/comeback_admin_panel/nginx/ssl/live/admin.comeback.uz/ && docker compose -f /path/to/docker-compose.yml exec -T nginx nginx -s reload
```
