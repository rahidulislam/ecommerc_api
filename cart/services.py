from cart.models import Cart, CartItem
from product.models import Product
from django.core.exceptions import ValidationError


class CartSerice:
    """Get or create cart for authenticated or anonymous user"""

    @staticmethod
    def get_or_create_cart(request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(
                session_key=session_key, defaults={"session_key": session_key}
            )
        return cart

    @staticmethod
    def add_item(cart, product_id, quantity):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist as e:
            raise ValidationError("Product does not exist.") from e
        if product.stock < quantity:
            raise ValidationError("Product is out of stock.")
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id, defaults={"quantity": quantity}
        )
        if not created:
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                raise ValidationError(f"cannot add more than {product.stock} items.")
            cart_item.quantity = new_quantity
            cart_item.save()
        return cart_item
    
    @staticmethod
    def update_item(item, quantity):
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        if item.product.stock < quantity:
            raise ValidationError(f"Only {item.product.stock} items in stock.")
        item.quantity = quantity
        item.save()
        return item
    
    @staticmethod
    def remove_item(item):
        item.delete()
