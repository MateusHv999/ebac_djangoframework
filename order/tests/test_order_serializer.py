import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebac_djangoframework.settings')
django.setup()

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from product.models import Product, Category
from order.models import Order
from order.serializers import OrderSerializer

class OrderSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Admin', password='1234')
        self.category = Category.objects.create(name='Roupas', slug='Vestidos')
    def test_total_when_order_has_price_should_return_price(self):
        # Configuration
        product1 = Product.objects.create(
            name='Vestido vermelho',
            price=100,
            stock=10,
            description='Perfeito para baladas',
            active=True
        )
        product1.categories.set([self.category])

        product2 = Product.objects.create(
            name='Vestido azul',
            price=200,
            stock=20,
            description='Perfeito para comemorações',
            active=True
        )
        product2.categories.set([self.category])

        order = Order.objects.create(user=self.user)
        order.products.set([product1, product2])

        # Execution
        serializer = OrderSerializer(order)
        data = serializer.data

        # Verify
        self.assertEqual(len(data['products']), 2)
        self.assertEqual(data['products'][0]['name'], 'Vestido vermelho')
        self.assertEqual(data['products'][1]['name'], 'Vestido azul')
        self.assertEqual(data['total'], 300)

    def test_getTotal_whenOrder_hasNoPrice_shouldNotReturnPrice(self):
        # Configuration
        product1 = Product.objects.create(
            name='Vestido vermelho',
            price=0,
            stock=10,
            description='Perfeito para baladas',
            active=True
        )
        product1.categories.set([self.category])

        product2 = Product.objects.create(
            name='Vestido azul',
            price=0,
            stock=20,
            description='Perfeito para comemorações',
            active=True
        )
        product2.categories.set([self.category])

        order = Order.objects.create(user=self.user)
        order.products.set([product1, product2])

        # Execution
        serializer = OrderSerializer(order)
        data = serializer.data

        # Verify
        self.assertEqual(len(data['products']), 2)
        self.assertEqual(data['products'][0]['name'], 'Vestido vermelho')
        self.assertEqual(data['products'][1]['name'], 'Vestido azul')
        self.assertNotIn(data['total'], data)
