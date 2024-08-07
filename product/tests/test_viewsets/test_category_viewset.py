import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebac_djangoframework.settings')
django.setup()

import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from product.factories import CategoryFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.categories = CategoryFactory(name="Technology")

    def test_order(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        self.assertEqual(category_data[0]['name'], self.categories.name)

    def test_create_category(self):
        data = json.dumps({
            'name': 'kitchen',
        })

        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_category = Category.objects.get(name='kitchen')

        self.assertEqual(created_category.name, 'kitchen')
