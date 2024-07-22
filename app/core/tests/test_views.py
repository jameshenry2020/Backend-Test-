from rest_framework.test import APITestCase, APIClient
from core.models import Category, Product, User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class ProductTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics')
        self.product_data = {
            'name': 'Laptop',
            'description': 'A powerful laptop',
            'price': '999.99',
            'category': self.category,
            'stock_qty': 3
        }
        self.product = Product.objects.create(**self.product_data)
        self.admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_create_product_endpoint(self):
        token = self.get_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        product_data = {
            'name': 'iphone 12',
            'description': 'A smart ios phone',
            'price': '999.99',
            'category': self.category.id,
            'stock_qty': 2
        }
        response = self.client.post('/api/products/', product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_product_list_endpoint(self):
        response = self.client.get(f'/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_product_detail_endpoint(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product_endpoint(self):
        token = self.get_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        updated_data = {'name': 'Updated Laptop', 'description': 'An updated powerful laptop', 'price': '1099.99', 'category': self.category.id}
        response = self.client.patch(f'/api/products/{self.product.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Laptop')
        self.assertEqual(self.product.description, 'An updated powerful laptop')