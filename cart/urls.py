from rest_framework.routers import DefaultRouter
from cart.views import CartItemViewSet

app_name = 'cart'

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cartitem')
urlpatterns = router.urls