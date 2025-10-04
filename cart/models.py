from django.db import models
from ecommerce_api.base_model import TimeStamp
# Create your models here.
class Cart(TimeStamp):
    """
    Shopping Cart model to hold products added by a user.
    Each cart is associated with a user and can contain multiple products.
    """
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, blank=True,null=True, related_name='cart')
    session_key = models.CharField(max_length=40, blank=True, null=True, help_text="Session identifier for guest users")

    def __str__(self):
        return f"Cart for {self.user.email if self.user else self.session_key}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    

class CartItem(TimeStamp):
    """
    Represents an item in the shopping cart.
    Each item is linked to a specific cart and product, along with quantity.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"
    
    @property
    def total_amount(self):
        return self.quantity * self.product.price