from rest_framework import generics, permissions

from apps.catalog.models import Product
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.user.is_staff or obj.user == request.user))


class ProductReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_id"]).select_related(
            "user",
            "product",
        )

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs["product_id"])
        serializer.save(user=self.request.user, product=product)


class ReviewDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]
    http_method_names = ["patch", "delete"]
    queryset = Review.objects.select_related("user", "product")
