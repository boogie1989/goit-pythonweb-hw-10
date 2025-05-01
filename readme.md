# Тема 10. Домашня робота

Створити REST API для зберігання та управління контактами. API повинен бути побудований з використанням інфраструктури FastAPI та повинен використовувати SQLAlchemy для управління базою даних.

## Технічний опис завданняТехнічний опис завдання

- Реалізуйте механізм аутентифікації в застосунку.

- Реалізуйте механізм авторизації за допомогою JWT-токенів, щоб усі операції з контактами проводились лише зареєстрованими користувачами.

- Користувач повинен мати доступ лише до своїх операцій з контактами.

- Реалізуйте механізм верифікації електронної пошти зареєстрованого користувача.

- Обмежте кількість запитів до маршруту користувача /me.

- Увімкніть CORS для свого REST API.

- Реалізуйте можливість оновлення аватара користувача (використовуйте сервіс Cloudinary).

## Як запустити

Створіть та налаштуйте конфігураційний `.env` файл у корені проєкту. Як приклад можете використати файл `example.env`.

```
DB_PORT=5432
DB_HOST=postgres
DB_USER=<DB_USER>
DB_PASSWORD=<DB_PASSWORD>
DB_NAME=<DB_NAME>
DB_URL=postgresql+asyncpg://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>

PORT=8000

JWT_SECRET=<JWT_SECRET>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600

CLOUDINARY_NAME=<CLOUDINARY_NAME>
CLOUDINARY_API_KEY=<CLOUDINARY_API_KEY>
CLOUDINARY_API_SECRET=<CLOUDINARY_API_SECRET>

MAIL_USERNAME=<MAIL_USERNAME>
MAIL_PASSWORD=<MAIL_PASSWORD>
MAIL_FROM=<MAIL_FROM>
MAIL_PORT=465
MAIL_SERVER=<MAIL_SERVER>
MAIL_FROM_NAME=<MAIL_FROM_NAME>
```

I потім запустіть Docker Compose

```
docker-compose up -d
```

API буде доступне за адресою: http://localhost:8000/docs
