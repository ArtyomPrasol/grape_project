# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app_web

# Копируем файлы зависимостей
COPY requirements.txt /app_web

# Устанавливаем Python зависимости
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . /app_web/

# Открываем порт
EXPOSE 5000 

# Запускаем приложение
CMD ["python", "run.py"]
