from rest_framework.test import APIClient
from django.test import TestCase


class ProductAPITests(TestCase):

    def test_list_products(self):
        client = APIClient()
        response = client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_create_category(self):
        client = APIClient()
        response = client.post('/categories/', {'name': 'New Category'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Category')

    def test_create_product(self):
        client = APIClient()

        response = client.post('/products/', {'name': 'New Product', 'price': 100, 'category': 'tezst'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Product')
