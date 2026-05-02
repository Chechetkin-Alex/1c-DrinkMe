from rest_framework import serializers

from apps.catalog.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "is_active"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_id",
            "name",
            "slug",
            "description",
            "product_type",
            "drink_size",
            "price",
            "stock",
            "is_active",
            "is_student_special",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
