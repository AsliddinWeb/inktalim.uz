# Server ga Deploy qilish

## 1. Serverda tayyorgarlik (Ubuntu 22.04)

```bash
# Paketlarni yangilash
sudo apt update && sudo apt upgrade -y

# Docker o'rnatish
sudo apt install -y docker.io docker-compose-plugin curl
sudo usermod -aG docker $USER
newgrp docker

# Nginx + Certbot o'rnatish
sudo apt install -y nginx certbot python3-certbot-nginx
```

## 2. Reponi clone qilish

```bash
cd /home/$USER
git clone https://github.com/SIZNING_USERNAME/REPO_NOMI.git inktalim
cd inktalim/project
```

## 3. `.env` fayl yaratish

```bash
cp .env.example .env
nano .env
```

`.env` da o'zgartirish kerak:
```env
POSTGRES_PASSWORD=SuperKuchliParol123!
DATABASE_URL=postgresql+asyncpg://postgres:SuperKuchliParol123!@db:5432/mini_udemy
SECRET_KEY=kamida-32-ta-tasodifiy-belgi-bu-yerga
ENVIRONMENT=production
ALLOWED_ORIGINS=https://inktalim.asliddin.me,https://www.inktalim.asliddin.me,https://inktalim.uz,https://www.inktalim.uz
FRONTEND_URL=https://inktalim.uz
VITE_API_URL=/api/v1
```

## 4. Docker containerlarni ishga tushirish

```bash
docker compose up --build -d
docker compose ps   # hammasi running ekanini tekshiring
```

## 5. Admin yaratish

```bash
docker compose exec backend python create_admin.py
```

## 6. Nginx sozlash

```bash
# Config faylni ko'chirish
sudo cp nginx/inktalim.conf /etc/nginx/sites-available/inktalim.conf
sudo ln -s /etc/nginx/sites-available/inktalim.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Syntax tekshirish
sudo nginx -t

# Nginx ishga tushirish
sudo systemctl restart nginx
```

## 7. SSL sertifikat olish (Let's Encrypt)

DNS recordlar serverga ko'rsatilganligini tekshiring, keyin:

```bash
sudo certbot --nginx \
  -d inktalim.asliddin.me \
  -d www.inktalim.asliddin.me \
  -d inktalim.uz \
  -d www.inktalim.uz
```

Email so'rasa — o'zingiznikini yozing.  
`Redirect HTTP to HTTPS` savol chiqsa — **2 (Yes)** tanlang.

```bash
# Sertifikat auto-renewal tekshirish
sudo certbot renew --dry-run
```

## 8. Yangi kodni deploy qilish (keyingi safar)

```bash
cd /home/$USER/inktalim/project
git pull origin main
docker compose up --build -d
```

---

## Foydali buyruqlar

```bash
# Loglarni ko'rish
docker compose logs -f backend
docker compose logs -f frontend

# Containerlarni qayta ishga tushirish
docker compose restart

# DB ga kirish
docker compose exec db psql -U postgres -d mini_udemy
```
