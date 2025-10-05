from cart.models import Cart, CartItem
from product.models import Product
from django.core.exceptions import ValidationError


class CartService:
    """Get or create cart for authenticated or anonymous user"""

    @staticmethod
    def get_or_create_cart(request):
        if request.user.is_authenticated:
            # Get or create user's cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            # if user was browsing anonymously, merge session cart.
            session_key = request.session.session_key
            if session_key:
                try:
                    session_cart = Cart.objects.get(session_key=session_key)
                    if session_cart != cart:
                        merged_count, warnings = CartService.merge_carts(
                            session_cart, cart
                        )
                        if warnings:
                            request.session["cart_merge_warnings"] = warnings
                        session_cart.delete()
                except Cart.DoesNotExist:
                    pass
            return cart
        else:
            # Anonymous: use session
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(
                session_key=session_key, defaults={"session_key": session_key}
            )
            return cart

    @staticmethod
    def merge_carts(session_cart, user_cart):
        """
        Merge session cart into user cart.
        If stock is insufficient, skip that item and collect warning.
        Returns: (merged_count, warnings)
        """
        merged_count = 0
        warnings = []
        for item in session_cart.items.all():
            product = item.product
            requested_quantity = item.quantity

            try:
                # check if product is still active and in stock
                if not product.is_active:
                    warnings.append(f"Product {product.name} is no longer available.")
                    continue
                if product.stock <= 0:
                    warnings.append(f"Product {product.name} is out of stock.")
                    continue
                # Determine how much can be added
                available_stock = product.stock
                user_cart_item = user_cart.items.filter(product=product).first()
                if user_cart_item:
                    max_possible = available_stock - user_cart_item.quantity
                else:
                    max_possible = available_stock
                if max_possible <= 0:
                    warnings.append(f"Not enough stock for {product.name}.")
                    continue
                # Add as much as possible
                actual_quantity = min(requested_quantity, max_possible)
                if user_cart_item:
                    user_cart_item.quantity += actual_quantity
                    user_cart_item.save()
                else:
                    CartItem.objects.create(
                        cart=user_cart, product=product, quantity=actual_quantity
                    )
                merged_count += 1
                # if partial merge
                if actual_quantity < requested_quantity:
                    warnings.append(
                        f"Only {actual_quantity}/{requested_quantity} of {product.name} added due to stock limits."
                    )
            except Exception as e:
                warnings.append(f"Error merging item {product.name}: {str(e)}")
        return merged_count, warnings

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
