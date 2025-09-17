from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from apps.stores.models import Store
from apps.products.models import Category, Brand, Product
from apps.customers.models import Customer

class BaseAPITestCase(APITestCase):
    """Classe base per test API"""
    
    def setUp(self):
        # Crea utente test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crea profilo customer
        self.customer = Customer.objects.create(
            user=self.user,
            phone='+39 333 1234567'
        )
        
        # Crea store test
        self.store = Store.objects.create(
            name='Test Store',
            slug='test-store',
            address='Via Test, 1',
            city='Milano',
            province='MI',
            postal_code='20121'
        )
        
        # Crea categoria e brand test
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.brand = Brand.objects.create(
            name='Test Brand',
            slug='test-brand'
        )

    def authenticate(self):
        """Autentica utente per i test"""
        self.client.force_authenticate(user=self.user)

class ProductAPITestCase(BaseAPITestCase):
    """Test per API prodotti"""
    
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(
            sku='TEST001',
            name='Test Product',
            slug='test-product',
            description='Test product description',
            category=self.category,
            brand=self.brand,
            base_price=100.00
        )

    def test_list_products(self):
        """Test lista prodotti"""
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_detail(self):
        """Test dettaglio prodotto"""
        response = self.client.get(f'/api/v1/products/{self.product.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_product_search(self):
        """Test ricerca prodotti"""
        response = self.client.get('/api/v1/products/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class AuthenticationTestCase(APITestCase):
    """Test per autenticazione"""
    
    def test_user_registration(self):
        """Test registrazione utente"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login(self):
        """Test login utente"""
        # Crea utente
        user = User.objects.create_user(
            username='logintest',
            password='testpass123'
        )
        
        data = {
            'username': 'logintest',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)