from django.db import models
from ecommerce_api.base_model import TimeStamp
# Create your models here.
class Order(TimeStamp):
    class STATUS_CHOICES(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELED = "CANCELED", "Canceled"
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,blank=True, null=True, related_name='orders')
    session_key = models.CharField(max_length=40, blank=True, null=True, help_text="Session identifier for guest users")
    guest_email = models.EmailField(blank=True, null=True, help_text="Email for guest users")
    guest_phone = models.CharField(max_length=15, blank=True, null=True, help_text="Phone number for guest users")
    billing_address = models.TextField()
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default="Bangladesh")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.PENDING)


    def __str__(self):
        if self.user:
            return f"Order {self.id} by {self.user.email}"
        elif self.guest_email:
            return f"Order {self.id} by {self.guest_email}"
        return f"Order {self.id} by session {self.session_key}"
    @property
    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())
class OrderItem(TimeStamp):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"

    @property
    def total_amount(self):
        return self.quantity * self.price