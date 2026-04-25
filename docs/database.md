# Проектирование базы данных

## Основные сущности

- User
- Category
- Product
- Cart
- CartItem
- Order
- OrderItem
- Review

## ER-диаграмма

```mermaid
erDiagram
    USER ||--o{ CART : owns
    USER ||--o{ ORDER : creates
    USER ||--o{ REVIEW : writes
    CATEGORY ||--o{ PRODUCT : contains
    PRODUCT ||--o{ CART_ITEM : added_as
    PRODUCT ||--o{ ORDER_ITEM : ordered_as
    PRODUCT ||--o{ REVIEW : receives
    CART ||--o{ CART_ITEM : contains
    ORDER ||--o{ ORDER_ITEM : contains

    USER {
        int id
        string email
        string username
        string password
        bool is_staff
    }

    CATEGORY {
        int id
        string name
        string slug
        bool is_active
    }

    PRODUCT {
        int id
        int category_id
        string name
        string slug
        string description
        string product_type
        decimal price
        int stock
        bool is_active
        bool is_student_special
    }

    CART {
        int id
        int user_id
        datetime created_at
        datetime updated_at
    }

    CART_ITEM {
        int id
        int cart_id
        int product_id
        int quantity
        string milk_type
    }

    ORDER {
        int id
        int user_id
        string status
        decimal total_price
        datetime created_at
        datetime updated_at
    }

    ORDER_ITEM {
        int id
        int order_id
        int product_id
        string product_name
        decimal price
        int quantity
        string milk_type
    }

    REVIEW {
        int id
        int user_id
        int product_id
        int rating
        string text
        datetime created_at
    }
```

## Типы продуктов

Планируемые типы товаров:

- `drink` - напиток
- `bakery` - выпечка
- `beans` - зерна
- `equipment` - аксессуар
- `machine_part` - деталь для кофемашины

## Статусы

Планируемые статусы заказа:

- `created` - заказ создан
- `paid` - заказ оплачен условно или подтвержден
- `in_progress` - заказ готовится
- `ready` - заказ готов к выдаче
- `completed` - заказ завершен
- `cancelled` - заказ отменен
