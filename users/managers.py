from django.contrib.auth.models import BaseUserManager
import importlib
class UserManager(BaseUserManager):
    def create_user(self,email,password, **extra_fields):
        """Creates and saves a User with the given email and password"""
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_customer(self,email,password,**extra_fields):
        """Create a patient with email and password"""
        customer_role = importlib.import_module('users.models').User.Role.CUSTOMER
        extra_fields.setdefault('role',customer_role)
        user = self.create_user(email,password,**extra_fields)
        return user

    def create_superuser(self,email,password,**extra_fields):
        """"Create a superuser with email and password"""
        superadmin_role = importlib.import_module('users.models').User.Role.ADMIN
        extra_fields.setdefault('role',superadmin_role)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        user = self.create_user(email,password,**extra_fields)
        return user