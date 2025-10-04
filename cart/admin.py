from django.contrib import admin
from cart.models import Cart, CartItem
# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "created_at", "updated_at")
    search_fields = ("user__email",)
    list_filter = ("created_at", "updated_at")
    inlines = [CartItemInline]
