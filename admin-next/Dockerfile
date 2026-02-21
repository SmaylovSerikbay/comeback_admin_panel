# Сборка
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
# npm install — чтобы сборка проходила при новых зависимостях в package.json без обновлённого lock-файла
RUN npm install

COPY . .

# При сборке в Docker API бэкенда доступен по имени сервиса web
ARG API_UPSTREAM=http://web:8000
ENV API_UPSTREAM=$API_UPSTREAM

RUN npm run build

# Продакшен
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
RUN mkdir -p ./public

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
