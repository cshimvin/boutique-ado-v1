from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    """ Show listed columns in the admin display """
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    # Order products by sku.
    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    """ Show listed columns in the admin display """
    list_display = (
        'friendly_name',
        'name',
    )

# Register the views on the admin app
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
