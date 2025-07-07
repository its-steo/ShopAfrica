from django.contrib import admin
from .models import Product, ProductImage, Subscriber

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percentage', 'coupon_code', 'quantity')
    search_fields = ('name', 'manufacturer', 'coupon_code')
    list_filter = ('discount_percentage',)
    inlines = [ProductImageInline]  # Show variety images inline

admin.site.register(ProductImage)
admin.site.register(Subscriber)
