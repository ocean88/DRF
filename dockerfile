# Используем базовый образ Python с поддержкой Poetry
FROM python:3.12-slim

# Устанавливаем переменную окружения для Python
ENV PYTHONUNBUFFERED 1

# Устанавливаем Poetry
RUN pip install poetry

# Создаем и устанавливаем директорию приложения в контейнере
RUN mkdir /app
WORKDIR /app

# Копируем файлы для установки зависимостей
COPY poetry.lock pyproject.toml /app/

# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем весь проект в контейнер
COPY . /app/

# Опционально: собираем статические файлы Django
# RUN python manage.py collectstatic --no-input

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
