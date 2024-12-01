FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /backend

# Копируем файлы проекта
COPY /backend /backend

# Копирование зависимостей и переменных окружения
COPY requirements.txt requirements.txt
COPY .env .env

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
