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
    combo_drink = ProductSerializer(read_only=True)
    combo_drink_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            is_active=True,
            product_type=Product.ProductType.DRINK,
            drink_size=Product.DrinkSize.SMALL,
        ),
        source="combo_drink",
        write_only=True,
        required=False,
        allow_null=True,
    )
    combo_bakery = ProductSerializer(read_only=True)
    combo_bakery_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            is_active=True,
            product_type=Product.ProductType.BAKERY,
        ),
        source="combo_bakery",
        write_only=True,
        required=False,
        allow_null=True,
    )
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_id",
            "combo_drink",
            "combo_drink_id",
            "combo_bakery",
            "combo_bakery_id",
            "quantity",
            "milk_type",
            "subtotal",
        ]

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
        combo_drink = attrs.get("combo_drink")
        combo_bakery = attrs.get("combo_bakery")
        if self.instance is not None:
            combo_drink = combo_drink or self.instance.combo_drink
            combo_bakery = combo_bakery or self.instance.combo_bakery
        if product is not None and quantity is not None and quantity > product.stock:
            raise serializers.ValidationError("На складе нет такого количества товара")
        if product is not None and product.is_student_special:
            request = self.context.get("request")
            if request is not None and not request.user.is_phystech_student:
                raise serializers.ValidationError("Комбо доступно только для почты МФТИ")
            if combo_drink is None or combo_bakery is None:
                raise serializers.ValidationError("Для комбо нужно выбрать кофе и выпечку")
            if combo_drink.drink_size != Product.DrinkSize.SMALL:
                raise serializers.ValidationError("В комбо доступен только маленький кофе")
            if quantity is not None and quantity > combo_drink.stock:
                raise serializers.ValidationError("На складе нет такого количества кофе")
            if quantity is not None and quantity > combo_bakery.stock:
                raise serializers.ValidationError("На складе нет такой выпечки")
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
