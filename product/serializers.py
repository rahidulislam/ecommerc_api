from rest_framework import serializers
from product.models import Category,Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name', 'slug', 'description', 'parent', )
        extra_kwargs = {
            'parent': {'write_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.children.exists():
            data['children'] = CategorySerializer(instance.children.all(), many=True).data 
        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name', 'slug', 'description', 'price', 'stock', 'help_text', 'image', )
        read_only_fields = ['created_at', 'updated_at', 'in_stock'] 
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['category'] = CategorySerializer(instance.category, many=True).data
    #     return data