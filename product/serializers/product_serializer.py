from rest_framework import serializers
from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "stock",
            "description",
            "active",
            "categories",
        ]
