# Django приложение с использованием Docker и Docker Compose

Этот репозиторий содержит пример Django приложения, настроенного для запуска в Docker контейнере с помощью Docker Compose.

## Требования

Для запуска этого проекта вам понадобится установленный Docker и Docker Compose на вашем компьютере.

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

## Запуск приложения

1. **Клонируйте репозиторий:**

   ```bash
   git clone <ссылка_на_репозиторий>
   cd <название_репозитория>

2 **Настройка переменных окружения**

Создайте файл .env в корне проекта и добавьте в него необходимые переменные окружения:
DJANGO_SECRET_KEY=your_secret_key_here

3 **Сборка и запуск контейнеров**
```bash
docker-compose up --build