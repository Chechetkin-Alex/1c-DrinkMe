from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.catalog.models import Category, Product
from apps.reviews.models import Review


class ReviewsApiTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            email="user@example.com",
            password="strongpass123",
        )
        category = Category.objects.create(name="Кофе", slug="coffee-reviews")
        self.product = Product.objects.create(
            category=category,
            name="Латте",
            slug="latte-reviews",
            product_type=Product.ProductType.DRINK,
            price="250.00",
            stock=3,
        )

    def test_review_list_is_public(self):
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            text="Вкусно",
        )

        response = self.client.get(f"/api/products/{self.product.id}/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["rating"], 5)

    def test_auth_user_can_create_review(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            f"/api/products/{self.product.id}/reviews/",
            {
                "rating": 5,
                "text": "Вкусно",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)

    def test_guest_cannot_create_review(self):
        response = self.client.post(
            f"/api/products/{self.product.id}/reviews/",
            {
                "rating": 5,
                "text": "Вкусно",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_user_cannot_edit_other_user_review(self):
        other_user = get_user_model().objects.create_user(
            username="other",
            email="other@example.com",
            password="strongpass123",
        )
        review = Review.objects.create(
            user=other_user,
            product=self.product,
            rating=4,
            text="Нормально",
        )
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            f"/api/reviews/{review.id}/",
            {"rating": 2},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
