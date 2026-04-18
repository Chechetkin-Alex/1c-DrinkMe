from django.contrib import admin

from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "product_type",
        "price",
        "stock",
        "is_student_special",
        "is_active",
    )
    list_filter = ("product_type", "is_active", "is_student_special", "category")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
