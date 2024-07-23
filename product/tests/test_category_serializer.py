import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebac_djangoframework.settings')
django.setup()

from rest_framework.test import APITestCase
from product.models import Product, Category
from product.serializers.category_serializer import CategorySerializer

class CategorySerializerTests(APITestCase):
    def setUp(self):
        self.clothes_category = Category.objects.create(name='Roupas', slug='Calças', description='Categoria para roupas', active= True)
        self.kitchen_category = Category.objects.create(name='Cozinha', slug='Utensilios',  description='Categoria para utensílios de cozinha', active= True)
    def test_category_serializer_whenCategory_created(self):
        #Execution
        serializer = CategorySerializer([self.clothes_category, self.kitchen_category], many=True)
        data = serializer.data

        #Verification

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['name'], 'Roupas')
        self.assertEqual(data[0]['slug'], 'Calças')
        self.assertEqual(data[0]['description'], 'Categoria para roupas')
        self.assertEqual(data[0]['active'], True)

        self.assertEqual(data[1]['name'], 'Cozinha')
        self.assertEqual(data[1]['slug'], 'Utensilios')
        self.assertEqual(data[1]['description'], 'Categoria para utensílios de cozinha')
        self.assertEqual(data[1]['active'], True)

    def test_category_serializer_whenCategory_created_hasError(self):
            # Execution
            serializer = CategorySerializer([self.clothes_category, self.kitchen_category], many=True)
            data = serializer.data

            # Verification

            self.assertEqual(len(data), 2)

            self.assertNotEqual(data[1]['name'], 'Roupas')
            self.assertNotEqual(data[1]['slug'], 'Calças')
            self.assertNotEqual(data[1]['description'], 'Categoria para roupas')
            self.assertNotEqual(data[1]['active'], False)

            self.assertNotEqual(data[0]['name'], 'Cozinha')
            self.assertNotEqual(data[0]['slug'], 'Utensilios')
            self.assertNotEqual(data[0]['description'], 'Categoria para utensílios de cozinha')
            self.assertNotEqual(data[0]['active'], False)