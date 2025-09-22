from django.db import models
from django.contrib.auth.models import AbstractUser
from ecommerce_api.base_model import TimeStamp
from .managers import UserManager

# Create your models here.

# Custom User Model
class User(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 1, "Admin"
        CUSTOMER = 2, "Customer"

    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.CUSTOMER)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

# Base Profile Model
class UserProfile(TimeStamp):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='%(class)s_profile')
    phone = models.CharField(max_length=15,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile',blank=True,null=True)

    def __str__(self):
        return self.user.email
