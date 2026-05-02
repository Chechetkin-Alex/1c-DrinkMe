from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.cart.services import add_product_to_cart, get_or_create_cart
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem


class OrdersApiTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            email="user@example.com",
            password="strongpass123",
        )
        category = Category.objects.create(name="Кофе", slug="coffee-orders")
        self.product = Product.objects.create(
            category=category,
            name="Латте",
            slug="latte-orders",
            product_type=Product.ProductType.DRINK,
            drink_size=Product.DrinkSize.SMALL,
            price="250.00",
            stock=3,
        )

    def test_order_requires_auth(self):
        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, 401)

    def test_user_can_create_order_from_cart(self):
        cart = get_or_create_cart(self.user)
        add_product_to_cart(cart, self.product, 2, milk_type="oat")
        self.client.force_authenticate(self.user)

        response = self.client.post("/api/orders/")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_price"], "500.00")
        self.assertEqual(response.data["items"][0]["milk_type"], "oat")
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(cart.items.count(), 0)

    def test_cannot_create_order_from_empty_cart(self):
        self.client.force_authenticate(self.user)

        response = self.client.post("/api/orders/")

        self.assertEqual(response.status_code, 400)

    def test_user_sees_only_own_orders(self):
        other_user = get_user_model().objects.create_user(
            username="other",
            email="other@example.com",
            password="strongpass123",
        )
        Order.objects.create(user=self.user, total_price="250.00")
        Order.objects.create(user=other_user, total_price="300.00")
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_change_order_status(self):
        admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="strongpass123",
        )
        order = Order.objects.create(user=self.user, total_price="250.00")
        self.client.force_authenticate(admin)

        response = self.client.patch(
            f"/api/orders/{order.id}/",
            {"status": Order.Status.READY},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.READY)
