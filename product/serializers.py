from rest_framework import serializers

from product.models import Category, Product


class CategorySerializerBase(serializers.ModelSerializer):
    """
    Base serializer for the Category model.
    Provides basic fields and write-only parent for use in other category serializers.
    """

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
    """
    Serializer for listing categories.
    Includes children (recursively) and product count for each category.
    """

    children = serializers.SerializerMethodField()
    product_count = serializers.IntegerField(source="products.count", read_only=True)

    class Meta(CategorySerializerBase.Meta):
        fields = CategorySerializerBase.Meta.fields + (
            "children",
            "product_count",
        )

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        if obj.children.exists():
            return CategorySerializerList(children, many=True).data
        return []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data["children"]:
            data.pop("children")
        return data

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if instance.children.exists():
    #         data["children"] = CategorySerializerBase(
    #             instance.children.all(), many=True
    #         ).data
    #     return data


class CategorySerializerRetrive(CategorySerializerList):
    """
    Serializer for retrieving a single category.
    Adds parent category details to the representation if present.
    """

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.parent is not None:
            data["parent"] = CategorySerializerBase(instance.parent).data
        return data


class CategorySerializerCreate(CategorySerializerBase):
    """
    Serializer for creating a category.
    Adds parent category details to the representation if present.
    """

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.parent is not None:
            data["parent"] = CategorySerializerBase(instance.parent).data
        return data


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Serializes all product fields and includes category details in the output.
    """

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "category",
            "price",
            "stock",
            "image",
            "in_stock",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = CategorySerializerBase(instance.category).data
        return data
