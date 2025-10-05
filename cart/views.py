from rest_framework import viewsets, status, permissions
from cart.models import CartItem
from cart.serializers import CartItemSerializer, AddToCartSerializer, UpdateCartItemSerializer
from cart.services import CartService
from rest_framework.response import Response
from django.core.exceptions import ValidationError


# Create your views here.


class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing cart items.

    Supports adding, updating, listing, and deleting items in a user's cart.
    Handles both authenticated and anonymous (session-based) users.

    Methods:
        get_serializer_class: Returns the appropriate serializer for create or other actions.
        get_queryset: Filters cart items for the current user's or session's cart.
        create: Adds a product to the cart, handling quantity and validation.
        update: Updates the quantity of a cart item.
        destroy: Removes an item from the cart.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action == "create":
            return AddToCartSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        cart = CartService.get_or_create_cart(self.request)
        # Check if merge happened and get warnings
        # We can store warnings in session during merge
        merge_warnings = request.session.pop("cart_merge_warnings", [])
        serailizer = self.get_serializer(cart.items.all(), many=True)
        response_data = {
            "items": serailizer.data,
            "total_items": len(serailizer.data),
            "total_price": cart.total_price,
            "merge_warnings": merge_warnings,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = CartService.get_or_create_cart(self.request)
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        try:
            item = CartService.add_item(cart, product_id, quantity)
            item_serializer = CartItemSerializer(item)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        quantity = serializer.validated_data.get("quantity", instance.quantity)
        try:
            item = CartService.update_item(instance, quantity)
            item_serializer = CartItemSerializer(item)
            return Response(item_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            CartService.remove_item(instance)
            return Response(
                {"details": "Item removed from cart."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
