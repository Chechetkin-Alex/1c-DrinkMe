from rest_framework import serializers

from apps.cart.models import Cart, CartItem


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def add_product_to_cart(
    cart,
    product,
    quantity,
    milk_type=CartItem.MilkType.REGULAR,
    combo_drink=None,
    combo_bakery=None,
):
    if quantity > product.stock:
        raise serializers.ValidationError("На складе нет такого количества товара")
    if product.is_student_special:
        if not cart.user.is_phystech_student:
            raise serializers.ValidationError("Комбо доступно только для почты МФТИ")
        if combo_drink is None or combo_bakery is None:
            raise serializers.ValidationError("Для комбо нужно выбрать кофе и выпечку")
        if quantity > combo_drink.stock:
            raise serializers.ValidationError("На складе нет такого количества кофе")
        if quantity > combo_bakery.stock:
            raise serializers.ValidationError("На складе нет такой выпечки")

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        milk_type=milk_type,
        combo_drink=combo_drink,
        combo_bakery=combo_bakery,
        defaults={"quantity": quantity},
    )
    if not created:
        new_quantity = item.quantity + quantity
        if new_quantity > product.stock:
            raise serializers.ValidationError("На складе нет такого количества товара")
        if product.is_student_special:
            if new_quantity > combo_drink.stock:
                raise serializers.ValidationError("На складе нет такого количества кофе")
            if new_quantity > combo_bakery.stock:
                raise serializers.ValidationError("На складе нет такой выпечки")
        item.quantity = new_quantity
        item.save(update_fields=["quantity"])
    return item
