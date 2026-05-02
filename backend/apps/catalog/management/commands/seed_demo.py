from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.catalog.models import Category, Product


class Command(BaseCommand):
    help = "Создает демо-категории, товары и администратора"

    def handle(self, *args, **options):
        categories = {
            "coffee": "Кофе",
            "bakery": "Выпечка",
            "beans": "Зерно",
            "equipment": "Аксессуары",
            "student-combo": "Студенческое комбо",
        }

        category_objects = {}
        for slug, name in categories.items():
            category_objects[slug], _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "is_active": True},
            )

        products = [
            {
                "category": "coffee",
                "name": "Латте",
                "slug": "latte-small",
                "description": "Мягкий кофейный напиток с молоком, маленький объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.SMALL,
                "price": "220.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Латте",
                "slug": "latte-medium",
                "description": "Мягкий кофейный напиток с молоком, средний объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.MEDIUM,
                "price": "260.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Латте",
                "slug": "latte-large",
                "description": "Мягкий кофейный напиток с молоком, большой объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.LARGE,
                "price": "310.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Капучино",
                "slug": "cappuccino-small",
                "description": "Классический кофе с плотной молочной пеной, маленький объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.SMALL,
                "price": "210.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Капучино",
                "slug": "cappuccino-medium",
                "description": "Классический кофе с плотной молочной пеной, средний объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.MEDIUM,
                "price": "250.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Капучино",
                "slug": "cappuccino-large",
                "description": "Классический кофе с плотной молочной пеной, большой объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.LARGE,
                "price": "300.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Флэт уайт",
                "slug": "flat-white-small",
                "description": "Более насыщенный кофе с молоком, маленький объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.SMALL,
                "price": "240.00",
                "stock": 25,
            },
            {
                "category": "coffee",
                "name": "Флэт уайт",
                "slug": "flat-white-medium",
                "description": "Более насыщенный кофе с молоком, средний объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.MEDIUM,
                "price": "280.00",
                "stock": 25,
            },
            {
                "category": "coffee",
                "name": "Флэт уайт",
                "slug": "flat-white-large",
                "description": "Более насыщенный кофе с молоком, большой объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.LARGE,
                "price": "330.00",
                "stock": 25,
            },
            {
                "category": "coffee",
                "name": "Американо",
                "slug": "americano-small",
                "description": "Черный кофе без молока, маленький объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.SMALL,
                "price": "160.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Американо",
                "slug": "americano-medium",
                "description": "Черный кофе без молока, средний объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.MEDIUM,
                "price": "190.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Американо",
                "slug": "americano-large",
                "description": "Черный кофе без молока, большой объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.LARGE,
                "price": "230.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Эспрессо",
                "slug": "espresso-small",
                "description": "Короткий крепкий кофе, маленький объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.SMALL,
                "price": "160.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Эспрессо",
                "slug": "espresso-medium",
                "description": "Короткий крепкий кофе, средний объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.MEDIUM,
                "price": "190.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Эспрессо",
                "slug": "espresso-large",
                "description": "Короткий крепкий кофе, большой объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.LARGE,
                "price": "220.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Раф",
                "slug": "raf-small",
                "description": "Сливочный кофейный напиток, маленький объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.SMALL,
                "price": "260.00",
                "stock": 20,
            },
            {
                "category": "coffee",
                "name": "Раф",
                "slug": "raf-medium",
                "description": "Сливочный кофейный напиток, средний объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.MEDIUM,
                "price": "310.00",
                "stock": 20,
            },
            {
                "category": "coffee",
                "name": "Раф",
                "slug": "raf-large",
                "description": "Сливочный кофейный напиток, большой объем",
                "product_type": Product.ProductType.DRINK,
                "drink_size": Product.DrinkSize.LARGE,
                "price": "360.00",
                "stock": 20,
            },
            {
                "category": "bakery",
                "name": "Круассан",
                "slug": "croissant",
                "description": "Слоеная выпечка к кофе",
                "product_type": Product.ProductType.BAKERY,
                "drink_size": Product.DrinkSize.NONE,
                "price": "180.00",
                "stock": 18,
            },
            {
                "category": "bakery",
                "name": "Булочка с корицей",
                "slug": "cinnamon-bun",
                "description": "Сладкая булочка с корицей",
                "product_type": Product.ProductType.BAKERY,
                "drink_size": Product.DrinkSize.NONE,
                "price": "170.00",
                "stock": 16,
            },
            {
                "category": "bakery",
                "name": "Сырок глазированный",
                "slug": "glazed-curd",
                "description": "Быстрый сладкий перекус",
                "product_type": Product.ProductType.BAKERY,
                "drink_size": Product.DrinkSize.NONE,
                "price": "90.00",
                "stock": 25,
            },
            {
                "category": "beans",
                "name": "Зерно Эфиопия 250 г",
                "slug": "ethiopia-beans-250",
                "description": "Светлая обжарка с ягодной кислотностью",
                "product_type": Product.ProductType.BEANS,
                "drink_size": Product.DrinkSize.NONE,
                "price": "650.00",
                "stock": 12,
            },
            {
                "category": "beans",
                "name": "Зерно Бразилия 250 г",
                "slug": "brazil-beans-250",
                "description": "Сбалансированная обжарка с ореховым вкусом",
                "product_type": Product.ProductType.BEANS,
                "drink_size": Product.DrinkSize.NONE,
                "price": "590.00",
                "stock": 12,
            },
            {
                "category": "beans",
                "name": "Дрип-пакеты 5 штук",
                "slug": "drip-bags-5",
                "description": "Порционный кофе для заваривания без кофемашины",
                "product_type": Product.ProductType.BEANS,
                "drink_size": Product.DrinkSize.NONE,
                "price": "420.00",
                "stock": 20,
            },
            {
                "category": "equipment",
                "name": "Фильтры для воронки",
                "slug": "paper-filters",
                "description": "Бумажные фильтры для домашнего кофе",
                "product_type": Product.ProductType.EQUIPMENT,
                "drink_size": Product.DrinkSize.NONE,
                "price": "320.00",
                "stock": 15,
            },
            {
                "category": "student-combo",
                "name": "Студенческое комбо",
                "slug": "student-combo",
                "description": "Маленький кофе и выпечка по сниженной цене для почты МФТИ",
                "product_type": Product.ProductType.COMBO,
                "drink_size": Product.DrinkSize.NONE,
                "price": "250.00",
                "stock": 30,
                "is_student_special": True,
            },
        ]

        active_slugs = [product["slug"] for product in products]
        Product.objects.exclude(slug__in=active_slugs).update(is_active=False)

        for product in products:
            category = category_objects[product.pop("category")]
            Product.objects.update_or_create(
                slug=product["slug"],
                defaults={**product, "category": category, "is_active": True},
            )

        user_model = get_user_model()
        admin, _ = user_model.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.email = "admin@example.com"
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("222333")
        admin.save()

        self.stdout.write(self.style.SUCCESS("Демо-данные добавлены"))
