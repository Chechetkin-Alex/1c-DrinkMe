from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APITestCase

from apps.catalog.models import Category, Product


class CatalogApiTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Кофе", slug="coffee")
        self.product = Product.objects.create(
            category=self.category,
            name="Латте",
            slug="latte",
            product_type=Product.ProductType.DRINK,
            price="250.00",
            stock=10,
        )

    def test_product_list_is_public(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], self.product.name)

    def test_product_list_can_be_filtered_by_category(self):
        other_category = Category.objects.create(name="Выпечка", slug="bakery")
        Product.objects.create(
            category=other_category,
            name="Круассан",
            slug="croissant",
            product_type=Product.ProductType.BAKERY,
            price="180.00",
            stock=5,
        )

        response = self.client.get("/api/products/?category=coffee")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "latte")

    def test_product_search_works_with_lowercase_russian_text(self):
        response = self.client.get("/api/products/?search=лат")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Латте")

    def test_guest_cannot_create_product(self):
        response = self.client.post(
            "/api/products/",
            {
                "category_id": self.category.id,
                "name": "Флэт уайт",
                "slug": "flat-white",
                "product_type": Product.ProductType.DRINK,
                "price": "280.00",
                "stock": 7,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_admin_can_create_product(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_authenticate(user)

        response = self.client.post(
            "/api/products/",
            {
                "category_id": self.category.id,
                "name": "Флэт уайт",
                "slug": "flat-white",
                "product_type": Product.ProductType.DRINK,
                "price": "280.00",
                "stock": 7,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)


class SeedDemoCommandTest(APITestCase):
    def test_seed_demo_creates_products_and_admin(self):
        call_command("seed_demo")

        self.assertTrue(Product.objects.filter(slug="latte-small").exists())
        self.assertTrue(Product.objects.filter(slug="cappuccino-small").exists())
        self.assertTrue(Product.objects.filter(slug="student-combo").exists())
        self.assertTrue(
            get_user_model().objects.filter(username="admin", is_staff=True).exists()
        )
