# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app_mobile

# Копируем файлы зависимостей
COPY requirements.txt /app_mobile

# Устанавливаем Python зависимости
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Копируем исходный код
COPY . /app_mobile/

# Открываем порт
EXPOSE 5001

# Запускаем приложение
CMD ["python", "app.py"]

