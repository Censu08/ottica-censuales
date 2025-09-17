import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from apps.stores.models import Store
from apps.products.models import Category, Brand, Product
from apps.customers.models import Customer
from apps.inventory.models import StoreInventory

class Command(BaseCommand):
    help = 'Popola il database con dati di esempio'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Cancella tutti i dati esistenti prima di popolare',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Cancellazione dati esistenti...')
            self.clear_data()

        self.stdout.write('Creazione dati di esempio...')
        
        # Crea stores
        stores = self.create_stores()
        self.stdout.write(f'✓ Creati {len(stores)} stores')
        
        # Crea categorie e brands
        categories = self.create_categories()
        brands = self.create_brands()
        self.stdout.write(f'✓ Creati {len(categories)} categorie e {len(brands)} brands')
        
        # Crea prodotti
        products = self.create_products(categories, brands)
        self.stdout.write(f'✓ Creati {len(products)} prodotti')
        
        # Crea inventario
        self.create_inventory(stores, products)
        self.stdout.write('✓ Creato inventario per tutti i stores')
        
        # Crea utenti clienti
        customers = self.create_customers(stores)
        self.stdout.write(f'✓ Creati {len(customers)} clienti')
        
        self.stdout.write(
            self.style.SUCCESS('Database popolato con successo!')
        )

    def clear_data(self):
        """Cancella dati esistenti"""
        StoreInventory.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()
        Customer.objects.all().delete()
        Store.objects.all().delete()

    def create_stores(self):
        """Crea stores di esempio"""
        stores_data = [
            {
                'name': 'Ottica Censuales Milano Centro',
                'slug': 'milano-centro',
                'address': 'Via Dante, 15',
                'city': 'Milano',
                'province': 'MI',
                'postal_code': '20121',
                'phone': '+39 02 1234567',
                'email': 'milano.centro@otticacensuales.it',
                'opening_hours': {
                    'lunedi': '9:00-19:00',
                    'martedi': '9:00-19:00',
                    'mercoledi': '9:00-19:00',
                    'giovedi': '9:00-19:00',
                    'venerdi': '9:00-19:00',
                    'sabato': '9:00-18:00',
                    'domenica': 'Chiuso'
                }
            },
            {
                'name': 'Ottica Censuales Corso Buenos Aires',
                'slug': 'corso-buenos-aires',
                'address': 'Corso Buenos Aires, 42',
                'city': 'Milano',
                'province': 'MI',
                'postal_code': '20124',
                'phone': '+39 02 7654321',
                'email': 'corso.buenosaires@otticacensuales.it',
                'opening_hours': {
                    'lunedi': '9:30-19:30',
                    'martedi': '9:30-19:30',
                    'mercoledi': '9:30-19:30',
                    'giovedi': '9:30-19:30',
                    'venerdi': '9:30-19:30',
                    'sabato': '9:30-19:00',
                    'domenica': 'Chiuso'
                }
            },
        ]
        
        stores = []
        for data in stores_data:
            store, created = Store.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            stores.append(store)
        
        return stores

    def create_categories(self):
        """Crea categorie di esempio"""
        categories_data = [
            {'name': 'Occhiali da Vista', 'slug': 'occhiali-vista', 'sort_order': 1},
            {'name': 'Occhiali da Sole', 'slug': 'occhiali-sole', 'sort_order': 2},
            {'name': 'Lenti a Contatto', 'slug': 'lenti-contatto', 'sort_order': 3},
            {'name': 'Liquidi per Lenti', 'slug': 'liquidi-lenti', 'sort_order': 4},
            {'name': 'Accessori', 'slug': 'accessori', 'sort_order': 5},
        ]
        
        categories = []
        for data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            categories.append(category)
        
        return categories

    def create_brands(self):
        """Crea brands di esempio"""
        brands_data = [
            {'name': 'Ray-Ban', 'slug': 'ray-ban'},
            {'name': 'Oakley', 'slug': 'oakley'},
            {'name': 'Persol', 'slug': 'persol'},
            {'name': 'Tom Ford', 'slug': 'tom-ford'},
            {'name': 'Gucci', 'slug': 'gucci'},
            {'name': 'Prada', 'slug': 'prada'},
            {'name': 'Versace', 'slug': 'versace'},
            {'name': 'Dolce & Gabbana', 'slug': 'dolce-gabbana'},
        ]
        
        brands = []
        for data in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            brands.append(brand)
        
        return brands

    def create_products(self, categories, brands):
        """Crea prodotti di esempio"""
        import random
        
        products_data = [
            {
                'name': 'Aviator Classic',
                'category': 'occhiali-sole',
                'brand': 'ray-ban',
                'base_price': Decimal('150.00'),
                'description': 'I classici occhiali da sole Aviator di Ray-Ban, una icona intramontabile dello stile.',
                'short_description': 'Occhiali da sole classici con montatura in metallo',
                'optical_attributes': {
                    'frame_material': 'metallo',
                    'lens_material': 'cristallo',
                    'gender': 'unisex',
                    'shape': 'aviator',
                    'protection': 'UV400'
                }
            },
            {
                'name': 'Wayfarer Original',
                'category': 'occhiali-sole',
                'brand': 'ray-ban',
                'base_price': Decimal('120.00'),
                'description': 'Gli originali Wayfarer Ray-Ban, perfetti per ogni occasione.',
                'short_description': 'Occhiali da sole iconici con montatura in acetato',
                'optical_attributes': {
                    'frame_material': 'acetato',
                    'lens_material': 'cristallo',
                    'gender': 'unisex',
                    'shape': 'quadrato',
                    'protection': 'UV400'
                }
            },
            # Aggiungi più prodotti...
        ]
        
        products = []
        category_dict = {c.slug: c for c in categories}
        brand_dict = {b.slug: b for b in brands}
        
        for data in products_data:
            category = category_dict.get(data['category'])
            brand = brand_dict.get(data['brand'])
            
            if category and brand:
                sku = f"{brand.name[:3].upper()}{random.randint(1000, 9999)}"
                slug = f"{brand.slug}-{data['name'].lower().replace(' ', '-')}"
                
                product, created = Product.objects.get_or_create(
                    sku=sku,
                    defaults={
                        'name': data['name'],
                        'slug': slug,
                        'description': data['description'],
                        'short_description': data['short_description'],
                        'category': category,
                        'brand': brand,
                        'base_price': data['base_price'],
                        'optical_attributes': data['optical_attributes'],
                    }
                )
                products.append(product)
        
        return products

    def create_inventory(self, stores, products):
        """Crea inventario per tutti i prodotti e stores"""
        import random
        
        for store in stores:
            for product in products:
                quantity = random.randint(5, 25)
                StoreInventory.objects.get_or_create(
                    store=store,
                    product=product,
                    defaults={
                        'quantity': quantity,
                        'is_online_available': True,
                        'store_price': product.base_price,
                        'minimum_stock': random.randint(2, 5)
                    }
                )

    def create_customers(self, stores):
        """Crea clienti di esempio"""
        customers_data = [
            {
                'username': 'mario.rossi',
                'email': 'mario.rossi@email.com',
                'first_name': 'Mario',
                'last_name': 'Rossi',
                'phone': '+39 333 1234567',
            },
            {
                'username': 'anna.verdi',
                'email': 'anna.verdi@email.com',
                'first_name': 'Anna',
                'last_name': 'Verdi',
                'phone': '+39 334 7654321',
            },
            {
                'username': 'luca.bianchi',
                'email': 'luca.bianchi@email.com',
                'first_name': 'Luca',
                'last_name': 'Bianchi',
                'phone': '+39 335 9876543',
            }
        ]
        
        customers = []
        for data in customers_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
            
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'phone': data['phone'],
                    'preferred_store': stores[0] if stores else None,
                }
            )
            customers.append(customer)
        
        return customers