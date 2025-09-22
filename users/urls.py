from django.urls import path,include

from rest_framework.routers import DefaultRouter
from .views import CustomerRegistrationViewSet

router = DefaultRouter()
router.register(r'register', CustomerRegistrationViewSet, basename='register')
urlpatterns = [
    path('', include(router.urls)),
]
