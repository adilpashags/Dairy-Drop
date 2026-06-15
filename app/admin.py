from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',  'name', 'locality', 'city', 'state', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products', 'quantity']

    def products(self, obj):
        link = reverse(
            "admin:app_product_change",
            args=[obj.product.pk]
        )

        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.product.title
        )

    products.short_description = "Product"

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class PlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'products', 'quantity',
                    'ordered_date', 'status', 'payments']

    def products(self, obj):
        link = reverse(
            "admin:app_product_change",
            args=[obj.product.pk]
        )
        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.product.title
        )

    def payments(self, obj):
        link = reverse(
            "admin:app_payment_change",
            args=[obj.payment.pk]
        )
        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.payment.razorpay_order_id
        )
        

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
    def product(self,obj):
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}"</a>',link,obj.product.title)

admin.site.unregister(Group)