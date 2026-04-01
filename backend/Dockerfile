# Backend uchun Dockerfile — Python 3.12 slim image asosida
FROM python:3.12-slim

# Ishchi katalog
WORKDIR /app

# Tizim paketlarini o'rnatish (asyncpg uchun kerakli kompilyator)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Avval requirements.txt ni ko'chirib, cache dan foydalanish
COPY requirements.txt .

# Python kutubxonalarini o'rnatish
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Qolgan kodlarni ko'chirish
COPY . .

# Backend 8000-portda ishlaydi
EXPOSE 8000

# Ishga tushirish buyrug'i (docker-compose override qiladi)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
