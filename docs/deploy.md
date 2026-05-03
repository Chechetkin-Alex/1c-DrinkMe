# Деплой

Этот документ описывает простой учебный деплой DrinkMe на Render.

## Почему Render

Render удобен для учебного проекта, потому что там можно поднять:

- Django-бэкенд
- React-фронтенд
- PostgreSQL-базу

На бесплатном тарифе есть ограничения:

- сервис может засыпать после простоя
- первый запрос после простоя может открываться дольше
- бесплатная PostgreSQL-база Render живет ограниченное время

Для защиты проекта в течение недели этого достаточно.

## Что уже подготовлено в проекте

- `backend/build.sh` ставит зависимости и собирает статику Django
- `backend/Procfile` запускает миграции, демо-данные и gunicorn
- `render.yaml` описывает базу, бэкенд и фронтенд для Render Blueprint
- `backend/config/settings.py` умеет подключаться к PostgreSQL через `DATABASE_URL`
- `backend/config/settings.py` умеет принимать запросы фронтенда через `DJANGO_CORS_ALLOWED_ORIGINS`
- `frontend/src/api/client.js` умеет брать адрес API из `VITE_API_BASE_URL`
- `frontend/.env.example` показывает пример адреса API для хостинга

## Что нужно сделать руками

1. Запушить репозиторий на GitHub

2. Зарегистрироваться или войти в Render

3. Создать Blueprint:

- открыть Render Dashboard
- выбрать `Blueprints`
- нажать `New Blueprint Instance`
- подключить GitHub
- выбрать репозиторий
- применить `render.yaml`

4. На этапе создания Render попросит значения для переменных с `sync: false`

Для бэкенда:

```text
DJANGO_ALLOWED_HOSTS=drinkme-backend.onrender.com
DJANGO_CORS_ALLOWED_ORIGINS=https://drinkme-frontend.onrender.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://drinkme-backend.onrender.com,https://drinkme-frontend.onrender.com
```

Для фронтенда:

```text
VITE_API_BASE_URL=https://drinkme-backend.onrender.com/api
```

Названия доменов нужно заменить на реальные адреса, которые Render выдаст твоим сервисам.

Если точные адреса еще неизвестны, можно сначала создать сервисы, потом открыть настройки каждого сервиса, поправить переменные окружения и запустить redeploy.

## Команды Render

Бэкенд собирается командой:

```bash
./build.sh
```

Бэкенд запускается командой:

```bash
python manage.py migrate && python manage.py seed_demo && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Фронтенд собирается командой:

```bash
npm install && npm run build
```

Фронтенд публикует папку:

```text
dist
```

## Как проверить после деплоя

1. Открыть адрес фронтенда

2. Проверить каталог

3. Зарегистрироваться на обычную почту

4. Зарегистрироваться на почту `@phystech.edu`

5. Проверить, что обычная почта не может добавить студенческое комбо

6. Проверить, что почта `@phystech.edu` может добавить студенческое комбо

7. Оформить заказ

8. Войти под админом

```text
admin
222333
```

9. Открыть заказы и поменять статус

10. Открыть Django admin

```text
https://drinkme-backend.onrender.com/admin/
```

11. Проверить товары, заказы и пользователей

## Почему фронт и бэк отдельно

Фронтенд это React-приложение. После сборки оно становится набором статических файлов:

- HTML
- CSS
- JavaScript

Такие файлы удобно отдавать через static hosting.

Бэкенд это Django-приложение. Оно должно:

- принимать HTTP-запросы
- проверять токены
- работать с PostgreSQL
- создавать заказы
- менять остатки
- хранить пользователей

Поэтому бэкенд запускается как отдельный серверный процесс через gunicorn.

Локально Vite помогает разработке и проксирует `/api` на Django. На хостинге такого dev proxy нет, поэтому фронту нужно явно сказать, где лежит публичный API:

```text
VITE_API_BASE_URL=https://drinkme-backend.onrender.com/api
```

А бэкенду нужно явно разрешить домен фронтенда:

```text
DJANGO_CORS_ALLOWED_ORIGINS=https://drinkme-frontend.onrender.com
```

Это нормальная схема для учебного проекта с React и Django REST API.
