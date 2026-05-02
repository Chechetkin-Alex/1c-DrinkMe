from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "price",
            "quantity",
            "combo_drink_name",
            "combo_bakery_name",
            "milk_type",
            "subtotal",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "username",
            "status",
            "total_price",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["total_price", "items", "created_at", "updated_at"]
