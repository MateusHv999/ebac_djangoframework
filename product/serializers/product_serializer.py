from rest_framework import serializers
from product.models.product import Product, Category
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    categories_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "stock",
            "description",
            "active",
            "categories",
            "categories_id",
        ]
    def create(self, validated_data):
        category_ids = validated_data.pop('categories_id', [])
        product = Product.objects.create(**validated_data)

        if category_ids:
            product.categories.set(category_ids)

        return product
