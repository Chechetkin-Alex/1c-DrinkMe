from rest_framework import permissions, viewsets

from apps.catalog.models import Category, Product
from apps.catalog.serializers import CategorySerializer, ProductSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Category.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.select_related("category")
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True, category__is_active=True)

        category = self.request.query_params.get("category")
        product_type = self.request.query_params.get("type")
        search = self.request.query_params.get("search")

        if category:
            queryset = queryset.filter(category__slug=category)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset
