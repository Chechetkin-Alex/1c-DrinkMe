from django.urls import path

from apps.reviews.views import ProductReviewListView, ReviewDetailView


urlpatterns = [
    path(
        "products/<int:product_id>/reviews/",
        ProductReviewListView.as_view(),
        name="product-reviews",
    ),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]

