# Frontend Dockerfile — Multi-stage build
# 1-bosqich: Node.js da build qilish
# 2-bosqich: Nginx da statik fayllarni serve qilish

# ─── 1-bosqich: Build ───────────────────────────────────────────────────────
FROM node:20.19-alpine3.21 AS builder

WORKDIR /app

# Avval package.json ni ko'chirib, npm install ni kesh qilish
COPY package.json package-lock.json* ./

# Kutubxonalarni o'rnatish
RUN npm install --frozen-lockfile

# Qolgan barcha fayllarni ko'chirish
COPY . .

# Build vaqtida API URL ni qabul qilish (docker-compose args orqali)
ARG VITE_API_URL=/api/v1
ENV VITE_API_URL=$VITE_API_URL

# Production build yaratish
RUN npm run build

# ─── 2-bosqich: Nginx bilan serve ────────────────────────────────────────────
FROM nginx:1.27-alpine3.21 AS runner

# Build natijasini nginx statik fayl papkasiga ko'chirish
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx SPA konfiguratsiyasini o'rnatish
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 80-portni ochish
EXPOSE 80

# Nginx ishga tushirish
CMD ["nginx", "-g", "daemon off;"]
