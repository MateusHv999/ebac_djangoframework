import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebac_djangoframework.settings')
django.setup()

import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from product.factories import CategoryFactory, ProductFactory
from product.models import Product
from order.factories import UserFactory

class TestProductViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(name="pro controller", price=200.00)

    def test_order(self):
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)[0]

        self.assertEqual(product_data['name'], self.product.name)
        self.assertEqual(product_data['price'], self.product.price)
        self.assertEqual(product_data['active'], self.product.active)

    def test_create_product(self):
        category = CategoryFactory()
        data = json.dumps({
            'name': 'notebook',
            'stock': 1,
            'price': 800,
            'categories_id': [category.id]
        })

        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_product = Product.objects.get(name='notebook')

        self.assertEqual(created_product.name, 'notebook')
        self.assertEqual(created_product.stock, 1)
        self.assertEqual(created_product.price, 800)



