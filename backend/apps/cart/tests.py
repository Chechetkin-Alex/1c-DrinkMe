from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.cart.models import CartItem
from apps.catalog.models import Category, Product


class CartApiTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            email="user@example.com",
            password="strongpass123",
        )
        category = Category.objects.create(name="Кофе", slug="coffee")
        self.product = Product.objects.create(
            category=category,
            name="Латте",
            slug="latte-cart",
            product_type=Product.ProductType.DRINK,
            price="250.00",
            stock=3,
        )

    def test_cart_requires_auth(self):
        response = self.client.get("/api/cart/")

        self.assertEqual(response.status_code, 401)

    def test_user_can_add_product_to_cart(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/api/cart/items/",
            {
                "product_id": self.product.id,
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["quantity"], 2)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_cart_returns_total_price(self):
        self.client.force_authenticate(self.user)
        self.client.post(
            "/api/cart/items/",
            {
                "product_id": self.product.id,
                "quantity": 2,
            },
            format="json",
        )

        response = self.client.get("/api/cart/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_price"], "500.00")

    def test_cannot_add_more_than_stock(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/api/cart/items/",
            {
                "product_id": self.product.id,
                "quantity": 4,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
