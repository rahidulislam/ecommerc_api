from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

app_name = 'order'
router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')
urlpatterns = router.urls