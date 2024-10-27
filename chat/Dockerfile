# Dockerfile для микросервиса chat

# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем все файлы проекта
COPY ./app /app

# Открываем порт для доступа
EXPOSE 8001

# Команда для запуска WebSocket сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
