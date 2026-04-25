from rest_framework import serializers

from apps.cart.models import Cart, CartItem
from apps.catalog.models import Product
from apps.catalog.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source="product",
        write_only=True,
    )
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "milk_type", "subtotal"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше нуля")
        return value

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")
        if self.instance is not None:
            product = product or self.instance.product
            quantity = quantity or self.instance.quantity
        if product is not None and quantity is not None and quantity > product.stock:
            raise serializers.ValidationError("На складе нет такого количества товара")
        return attrs


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price", "created_at", "updated_at"]
