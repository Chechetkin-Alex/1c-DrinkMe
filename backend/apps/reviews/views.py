from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.catalog.models import Product
from apps.orders.models import OrderItem
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

    def create(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs["product_id"])
        has_order = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
        ).exists()
        if not has_order:
            return Response(
                {"detail": "Отзыв можно оставить только после покупки товара"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        existing_review = Review.objects.filter(
            user=request.user,
            product=product,
        ).first()
        serializer = self.get_serializer(
            existing_review,
            data=request.data,
            partial=existing_review is not None,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product=product)
        response_status = status.HTTP_200_OK if existing_review else status.HTTP_201_CREATED
        return Response(serializer.data, status=response_status)


class ReviewDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]
    http_method_names = ["patch", "delete"]
    queryset = Review.objects.select_related("user", "product")
