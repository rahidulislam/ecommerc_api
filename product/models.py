from django.db import models
from django.urls import reverse
from ecommerce_api.base_model import TimeStamp
from django.core.validators import MinValueValidator

# Create your models here.
class Category(TimeStamp):
    """
    Product Category (e.g., Electronics, Books, Clothing)
    Supports subcategories via parent-child relationship
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="URL friendly name")
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', help_text="for sub-categories")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.parent} -> {self.name}"
        return self.name
    
class Product(TimeStamp):
    """
    Represents a product in the e-commerce platform.

    Fields:
        name: The name of the product.
        slug: URL-friendly unique identifier for the product.
        description: Detailed description of the product.
        price: Price of the product (must be non-negative).
        stock: Number of items available in stock (must be non-negative).
        category: Foreign key to the Category the product belongs to.
        image: Optional image of the product.

    Methods:
        __str__: Returns the product's name.
        in_stock: Returns True if the product is in stock, False otherwise.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="URL friendly name")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)], help_text="Number of items available in stock")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]
    def __str__(self):
        return self.name
    
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})
