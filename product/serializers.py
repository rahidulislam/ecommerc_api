from rest_framework import serializers
from product.models import Category, Product


class CategorySerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "parent",
        )
        extra_kwargs = {
            "parent": {"write_only": True},
        }

class CategorySerializerList(CategorySerializerBase):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.children.exists():
            data["children"] = CategorySerializerBase(
                instance.children.all(), many=True
            ).data
        return data

class CategorySerializerRetrive(CategorySerializerList):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.parent is not None:
            data["parent"] = CategorySerializerBase(instance.parent).data
        return data

class CategorySerializerCreate(CategorySerializerBase):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.parent is not None:
            data["parent"] = CategorySerializerBase(instance.parent).data
        return data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "image",
        )
        read_only_fields = ["created_at", "updated_at", "in_stock"]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['category'] = CategorySerializer(instance.category, many=True).data
    #     return data
