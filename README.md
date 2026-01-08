# microservice-architecture

## Приложение для microservice-architecture

Этот репозиторий содержит простое веб приложение для обучения микросервисной разработке.
FastAPI приложение с эндпоинтами для работы с изерами, статьями и комментариями


Сделанный по обучаемому примеру с сайта:
https://gist.github.com/ayusavin/4eda9e9e1dbcdb0929ec168616d2cf0e#file-lab4-md

Swagger:
https://microservice-architecture-latest-75wy.onrender.com/api/v1/swagger


## Необходимые инструменты 
* Python (3.12.6)
* Poetry (1.8.3)
* docker


# Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Dmitry505/microservice-architecture

2. Установите зависимости:

    ```bash
    poetry install

3. Перемещений в нужный каталог

    ```bash
   cd .\microservice-architecture
   
4. Создание .env

    ```bash
   copy .env.example .env
   # or 
   cp .env.example .env

5. Запуск сервера

    ```bash
    docker-compose --profile dev --profile production up -d --build
