import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebac_djangoframework.settings')
django.setup()

import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import OrderFactory, UserFactory
from product.models import Product
from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.categories = CategoryFactory(name="Technology")
        self.product = ProductFactory(name="mouse", stock=1, price=100, categories=[self.categories])
        self.order = OrderFactory(products=[self.product])

    def test_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_data = json.loads(response.content)[0]

        self.assertEqual(order_data['products'][0]['name'], self.product.name)
        self.assertEqual(order_data['products'][0]['price'], self.product.price)
        self.assertEqual(order_data['products'][0]['active'], self.product.active)
        self.assertEqual(order_data['products'][0]['categories'][0]['name'], self.categories.name)

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({
            'products_id': [product.id],
            'user': user.id
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.get(user=user)
