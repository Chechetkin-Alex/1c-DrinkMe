# REST API 

Основной префикс `/api/`

## Авторизация

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/me/
```

Регистрация и вход возвращают токен. Фронт отправляет его в заголовке:

```text
Authorization: Token <token>
```

## Категории

```
GET    /api/categories/
POST   /api/categories/
GET    /api/categories/{id}/
PATCH  /api/categories/{id}/
DELETE /api/categories/{id}/
```

Для гостей доступны `GET`. Изменение категорий доступно администратору.

## Товары

```
GET    /api/products/
POST   /api/products/
GET    /api/products/{id}/
PATCH  /api/products/{id}/
DELETE /api/products/{id}/
```

Пример параметров:

```
?category=coffee
?type=drink
?search=латте
```

Создавать и менять товары может только администратор.

## Корзина

```
GET    /api/cart/
POST   /api/cart/items/
PATCH  /api/cart/items/{id}/
DELETE /api/cart/items/{id}/
DELETE /api/cart/clear/
```

Корзина доступна только авторизованному пользователю.

Пример добавления товара:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

## Заказы

```
GET   /api/orders/
POST  /api/orders/
GET   /api/orders/{id}/
PATCH /api/orders/{id}/
```

`POST /api/orders/` создает заказ из текущей корзины.

Пользователь видит только свои заказы. Администратор видит все заказы и может менять статус.

Пример ответа:

```json
{
  "id": 67,
  "status": "created",
  "total_price": "550",
  "items": [
    {
      "product_name": "Латте на кокосовом",
      "price": "350",
      "quantity": 1
    },
    {
      "product_name": "Дрип пакет 100g",
      "price": "200",
      "quantity": 1
    }
  ]
}
```

## Отзывы

```
GET    /api/products/{product_id}/reviews/
POST   /api/products/{product_id}/reviews/
PATCH  /api/reviews/{id}/
DELETE /api/reviews/{id}/
```
