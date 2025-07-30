#!/usr/bin/env python
"""
Create migrations for the Product model.
Run this script after adding the Product model to create the necessary database migrations.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def create_migrations():
    """Create and apply migrations for the Product model"""
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgriMarket.settings')
    
    # Setup Django
    django.setup()
    
    print("🌱 Creating Product model migrations...")
    
    # Make migrations for the market app
    print("\n📝 Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations', 'market'])
    
    # Apply migrations
    print("\n🔄 Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n✅ Product model migrations complete!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Login as a farmer")
    print("3. Visit: http://127.0.0.1:8000/dashboard/ to see the updated dashboard")
    print("4. Click 'Add Product' to start listing products")
    
    # Create sample products
    create_sample_products()

def create_sample_products():
    """Create sample products for testing"""
    from market.models import User, Product
    
    print("\n📦 Creating sample products...")
    
    # Get the sample farmer user
    try:
        farmer = User.objects.get(username='farmer1')
        
        # Create sample products if they don't exist
        sample_products = [
            {
                'name': 'Fresh Organic Tomatoes',
                'category': 'Vegetables',
                'price': 3.50,
                'quantity': 50,
                'description': 'Vine-ripened organic tomatoes, perfect for salads and cooking. Grown without pesticides on our family farm.',
                'location': 'Green Valley Farm, California'
            },
            {
                'name': 'Sweet Corn',
                'category': 'Vegetables', 
                'price': 0.75,
                'quantity': 100,
                'description': 'Fresh sweet corn picked daily. Perfect for grilling or boiling. Non-GMO variety.',
                'location': 'Sunny Acres Farm, California'
            },
            {
                'name': 'Farm Fresh Eggs',
                'category': 'Dairy',
                'price': 4.00,
                'quantity': 25,
                'description': 'Free-range chicken eggs from happy hens. Rich, golden yolks and excellent for baking.',
                'location': 'Happy Hen Farm, California'
            }
        ]
        
        for product_data in sample_products:
            if not Product.objects.filter(farmer=farmer, name=product_data['name']).exists():
                Product.objects.create(farmer=farmer, **product_data)
                print(f"✅ Created sample product: {product_data['name']}")
        
        print(f"\n🎉 Sample products created for farmer: {farmer.username}")
        
    except User.DoesNotExist:
        print("\n⚠️  Sample farmer user not found. Run the setup_database.py script first.")

if __name__ == '__main__':
    create_migrations()
