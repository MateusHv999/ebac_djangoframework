import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebac_djangoframework.settings')
django.setup()

from rest_framework.test import APITestCase
from product.models import Product, Category
from product.serializers.product_serializer import ProductSerializer

class ProductSerializerTests(APITestCase):
   def setUp(self):
    self.clothes_category = Category.objects.create(name='Roupas', slug='Calças')
    self.kitchen_category = Category.objects.create(name='Cozinha', slug='Utensilios')

   def test_product_serializer_whenProduct_created(self):
       #Configuration
       product = Product.objects.create(
           name='Calça jeans',
           price=100,
           stock=10,
           description='Calça jeans confortável',
           active=True
       )
       product.categories.add(self.clothes_category)

       #Execution
       serializer = ProductSerializer(product)
       data = serializer.data

       #Verification
       self.assertEqual(data['name'], 'Calça jeans' )
       self.assertEqual(data['categories'][0]['name'], 'Roupas')

   def test_product_serializer_whenProduct_created_has_Error(self):
       # Configuration
       product = Product.objects.create(
           name='Colher de prata',
           price=100,
           stock=10,
           description='Um utensilio para a cozinha',
           active=True
       )
       product.categories.add(self.kitchen_category)

       # Execution
       serializer = ProductSerializer(product)
       data = serializer.data

       # Verification
       self.assertNotEqual(data['name'], 'Calça jeans')
       self.assertNotEqual(data['categories'][0]['name'], 'Roupas')

