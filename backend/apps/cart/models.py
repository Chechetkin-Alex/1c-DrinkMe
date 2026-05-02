from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.select_related("product"))


class CartItem(models.Model):
    class MilkType(models.TextChoices):
        REGULAR = "regular", "Regular"
        ALTERNATIVE = "alternative", "Alternative"
        OAT = "oat", "Oat"
        COCONUT = "coconut", "Coconut"
        BANANA = "banana", "Banana"
        ALMOND = "almond", "Almond"
        NONE = "none", "No milk"

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    combo_drink = models.ForeignKey(
        "catalog.Product",
        on_delete=models.SET_NULL,
        related_name="combo_drink_cart_items",
        blank=True,
        null=True,
    )
    combo_bakery = models.ForeignKey(
        "catalog.Product",
        on_delete=models.SET_NULL,
        related_name="combo_bakery_cart_items",
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    milk_type = models.CharField(
        max_length=30,
        choices=MilkType.choices,
        default=MilkType.REGULAR,
    )

    class Meta:
        unique_together = (
            "cart",
            "product",
            "milk_type",
            "combo_drink",
            "combo_bakery",
        )
        ordering = ["id"]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}, milk: {self.milk_type}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
