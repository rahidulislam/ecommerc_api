from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


# User Serializer
class UserSerializerBase(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class CustomerSerializer(UserSerializerBase):
    """Create Customer Serializer"""

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["role"] = user.get_role_display()

        # ...

        return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)

    #     # Add extra responses here
    #     data["user"] = {
    #         "id": self.user.id,
    #         "email": self.user.email,
    #         "first_name": self.user.first_name,
    #         "last_name": self.user.last_name,
    #         "role": self.user.role,
    #     }
    #     return data
