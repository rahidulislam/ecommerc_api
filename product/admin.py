from django.contrib import admin
from .models import Category, Product
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at',]
    list_filter = ['parent', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category','price','stock', 'is_active', 'created_at',]
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    