#!/usr/bin/env python
"""
Add more sample products for better testing of the search and filter functionality.
"""

import os
import sys
import django
from decimal import Decimal

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgriMarket.settings')
    django.setup()

def create_more_sample_products():
    """Create additional sample products for testing"""
    from market.models import User, Product
    
    print("🌱 Adding more sample products for testing...")
    
    # Get or create sample farmers
    farmers_data = [
        {
            'username': 'farmer2',
            'email': 'farmer2@example.com',
            'password': 'testpass123',
            'full_name': 'Maria Rodriguez',
            'phone_number': '+1555123456',
            'user_type': 'Farmer'
        },
        {
            'username': 'farmer3',
            'email': 'farmer3@example.com',
            'password': 'testpass123',
            'full_name': 'David Chen',
            'phone_number': '+1555789012',
            'user_type': 'Farmer'
        }
    ]
    
    farmers = []
    for farmer_data in farmers_data:
        farmer, created = User.objects.get_or_create(
            username=farmer_data['username'],
            defaults=farmer_data
        )
        if created:
            farmer.set_password(farmer_data['password'])
            farmer.save()
            print(f"✅ Created farmer: {farmer.username}")
        farmers.append(farmer)
    
    # Get existing farmer1
    try:
        farmer1 = User.objects.get(username='farmer1')
        farmers.insert(0, farmer1)
    except User.DoesNotExist:
        print("⚠️  farmer1 not found, creating...")
        farmer1 = User.objects.create_user(
            username='farmer1',
            email='farmer1@example.com',
            password='testpass123',
            full_name='John Farmer',
            phone_number='+1234567890',
            user_type='Farmer'
        )
        farmers.insert(0, farmer1)
    
    # Sample products data
    products_data = [
        # Farmer 1 products
        {
            'farmer': farmers[0],
            'name': 'Organic Carrots',
            'category': 'Vegetables',
            'price': Decimal('2.50'),
            'quantity': 75,
            'description': 'Sweet, crunchy organic carrots perfect for snacking or cooking. Grown in rich soil without pesticides.',
            'location': 'Green Valley Farm, California'
        },
        {
            'farmer': farmers[0],
            'name': 'Fresh Spinach',
            'category': 'Vegetables',
            'price': Decimal('4.00'),
            'quantity': 30,
            'description': 'Tender baby spinach leaves, perfect for salads or smoothies. Harvested daily for maximum freshness.',
            'location': 'Green Valley Farm, California'
        },
        
        # Farmer 2 products
        {
            'farmer': farmers[1],
            'name': 'Strawberries',
            'category': 'Fruits',
            'price': Decimal('6.00'),
            'quantity': 40,
            'description': 'Sweet, juicy strawberries picked at peak ripeness. Perfect for desserts or eating fresh.',
            'location': 'Berry Fields Farm, Oregon'
        },
        {
            'farmer': farmers[1],
            'name': 'Organic Apples',
            'category': 'Fruits',
            'price': Decimal('3.25'),
            'quantity': 100,
            'description': 'Crisp, sweet organic apples from our heritage orchard. Multiple varieties available.',
            'location': 'Berry Fields Farm, Oregon'
        },
        {
            'farmer': farmers[1],
            'name': 'Fresh Basil',
            'category': 'Herbs',
            'price': Decimal('2.00'),
            'quantity': 25,
            'description': 'Aromatic fresh basil perfect for cooking. Grown in our greenhouse for year-round availability.',
            'location': 'Berry Fields Farm, Oregon'
        },
        
        # Farmer 3 products
        {
            'farmer': farmers[2],
            'name': 'Brown Rice',
            'category': 'Grains',
            'price': Decimal('4.50'),
            'quantity': 200,
            'description': 'Nutritious whole grain brown rice. Grown using sustainable farming practices.',
            'location': 'Golden Grain Farm, Texas'
        },
        {
            'farmer': farmers[2],
            'name': 'Quinoa',
            'category': 'Grains',
            'price': Decimal('8.00'),
            'quantity': 50,
            'description': 'High-protein quinoa grain, perfect for healthy meals. Gluten-free and nutrient-dense.',
            'location': 'Golden Grain Farm, Texas'
        },
        {
            'farmer': farmers[2],
            'name': 'Goat Cheese',
            'category': 'Dairy',
            'price': Decimal('12.00'),
            'quantity': 15,
            'description': 'Creamy, artisanal goat cheese made from our happy goats. Perfect for salads and appetizers.',
            'location': 'Golden Grain Farm, Texas'
        },
        {
            'farmer': farmers[2],
            'name': 'Bell Peppers',
            'category': 'Vegetables',
            'price': Decimal('3.75'),
            'quantity': 60,
            'description': 'Colorful bell peppers in red, yellow, and green. Sweet and crunchy, perfect for cooking.',
            'location': 'Golden Grain Farm, Texas'
        },
        {
            'farmer': farmers[2],
            'name': 'Rosemary',
            'category': 'Herbs',
            'price': Decimal('1.50'),
            'quantity': 35,
            'description': 'Fresh rosemary sprigs with intense aroma. Perfect for seasoning meats and vegetables.',
            'location': 'Golden Grain Farm, Texas'
        }
    ]
    
    # Create products
    created_count = 0
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            farmer=product_data['farmer'],
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            created_count += 1
            print(f"✅ Created product: {product.name} by {product.farmer.username}")
    
    print(f"\n🎉 Created {created_count} new sample products!")
    print(f"📊 Total products in database: {Product.objects.count()}")
    
    print("\n🔑 Test the search and filter functionality:")
    print("- Search for 'organic' to find organic products")
    print("- Filter by 'Vegetables' category")
    print("- Set price range from $2 to $5")
    print("- Search by location 'California' or 'Oregon'")

if __name__ == '__main__':
    setup_django()
    create_more_sample_products()
