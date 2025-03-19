# Используем последний стабильный Python-образ
FROM python:3.10-slim-bullseye

# Устанавливаем основные пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        musl-dev \
        libffi-dev \
        libssl-dev \
        openssl \
        git \
        libc-dev \
        build-essential \
        libpq-dev \
        netcat

# Устанавливаем Pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install drf-yasg
# Создаем рабочую директорию
WORKDIR /app

# Копируем требования и устанавливаем зависимости
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Копируем весь код проекта
COPY . /app/

# Экспортируем порт 8000
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]