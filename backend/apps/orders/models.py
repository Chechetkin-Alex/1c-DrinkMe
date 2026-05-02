from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        PAID = "paid", "Paid"
        IN_PROGRESS = "in_progress", "In progress"
        READY = "ready", "Ready"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.CREATED,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    class MilkType(models.TextChoices):
        REGULAR = "regular", "Regular"
        ALTERNATIVE = "alternative", "Alternative"
        OAT = "oat", "Oat"
        COCONUT = "coconut", "Coconut"
        BANANA = "banana", "Banana"
        ALMOND = "almond", "Almond"
        NONE = "none", "No milk"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    product_name = models.CharField(max_length=160)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    combo_drink_name = models.CharField(max_length=160, blank=True)
    combo_bakery_name = models.CharField(max_length=160, blank=True)
    milk_type = models.CharField(
        max_length=30,
        choices=MilkType.choices,
        default=MilkType.REGULAR,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
