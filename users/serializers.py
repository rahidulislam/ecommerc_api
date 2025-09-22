from rest_framework import serializers
from user_account.models import User, UserProfile

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'role', 'is_active', 'date_joined']