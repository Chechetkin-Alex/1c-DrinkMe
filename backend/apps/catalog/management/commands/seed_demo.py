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
                "slug": "latte",
                "description": "Мягкий кофейный напиток с молоком",
                "product_type": Product.ProductType.DRINK,
                "price": "250.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Капучино",
                "slug": "cappuccino",
                "description": "Классический кофе с плотной молочной пеной",
                "product_type": Product.ProductType.DRINK,
                "price": "240.00",
                "stock": 30,
            },
            {
                "category": "coffee",
                "name": "Флэт уайт",
                "slug": "flat-white",
                "description": "Более насыщенный кофе с молоком",
                "product_type": Product.ProductType.DRINK,
                "price": "270.00",
                "stock": 25,
            },
            {
                "category": "coffee",
                "name": "Американо",
                "slug": "americano",
                "description": "Черный кофе без молока",
                "product_type": Product.ProductType.DRINK,
                "price": "180.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Эспрессо",
                "slug": "espresso",
                "description": "Короткий крепкий кофе",
                "product_type": Product.ProductType.DRINK,
                "price": "160.00",
                "stock": 40,
            },
            {
                "category": "coffee",
                "name": "Раф",
                "slug": "raf",
                "description": "Сливочный кофейный напиток",
                "product_type": Product.ProductType.DRINK,
                "price": "290.00",
                "stock": 20,
            },
            {
                "category": "bakery",
                "name": "Круассан",
                "slug": "croissant",
                "description": "Слоеная выпечка к кофе",
                "product_type": Product.ProductType.BAKERY,
                "price": "180.00",
                "stock": 18,
            },
            {
                "category": "bakery",
                "name": "Булочка с корицей",
                "slug": "cinnamon-bun",
                "description": "Сладкая булочка с корицей",
                "product_type": Product.ProductType.BAKERY,
                "price": "170.00",
                "stock": 16,
            },
            {
                "category": "bakery",
                "name": "Сырок глазированный",
                "slug": "glazed-curd",
                "description": "Быстрый сладкий перекус",
                "product_type": Product.ProductType.BAKERY,
                "price": "90.00",
                "stock": 25,
            },
            {
                "category": "beans",
                "name": "Зерно Эфиопия 250 г",
                "slug": "ethiopia-beans-250",
                "description": "Светлая обжарка с ягодной кислотностью",
                "product_type": Product.ProductType.BEANS,
                "price": "650.00",
                "stock": 12,
            },
            {
                "category": "beans",
                "name": "Зерно Бразилия 250 г",
                "slug": "brazil-beans-250",
                "description": "Сбалансированная обжарка с ореховым вкусом",
                "product_type": Product.ProductType.BEANS,
                "price": "590.00",
                "stock": 12,
            },
            {
                "category": "beans",
                "name": "Дрип-пакеты 5 штук",
                "slug": "drip-bags-5",
                "description": "Порционный кофе для заваривания без кофемашины",
                "product_type": Product.ProductType.BEANS,
                "price": "420.00",
                "stock": 20,
            },
            {
                "category": "equipment",
                "name": "Фильтры для воронки",
                "slug": "paper-filters",
                "description": "Бумажные фильтры для домашнего кофе",
                "product_type": Product.ProductType.EQUIPMENT,
                "price": "320.00",
                "stock": 15,
            },
            {
                "category": "student-combo",
                "name": "Студенческое комбо",
                "slug": "student-combo",
                "description": "Кофе и булочка по сниженной цене для почты МФТИ",
                "product_type": Product.ProductType.DRINK,
                "price": "199.00",
                "stock": 30,
                "is_student_special": True,
            },
        ]

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
