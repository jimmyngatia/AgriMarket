#!/usr/bin/env python
"""
Database setup script for AgriMarket Django project.
Run this script to create and migrate the database.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_database():
    """Set up the database with migrations and create superuser"""
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgriMarket.settings')
    
    # Setup Django
    django.setup()
    
    print("🌱 Setting up AgriMarket database...")
    
    # Make migrations
    print("\n📝 Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Apply migrations
    print("\n🔄 Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n✅ Database setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py createsuperuser (to create admin user)")
    print("2. Run: python manage.py runserver (to start the development server)")
    print("3. Visit: http://127.0.0.1:8000/ (to view the application)")
    
    # Create some sample data
    create_sample_users()

def create_sample_users():
    """Create sample users for testing"""
    from market.models import User
    
    print("\n👥 Creating sample users...")
    
    # Create sample farmer
    if not User.objects.filter(username='farmer1').exists():
        farmer = User.objects.create_user(
            username='farmer1',
            email='farmer@example.com',
            password='testpass123',
            full_name='John Farmer',
            phone_number='+1234567890',
            user_type='Farmer'
        )
        print(f"✅ Created farmer: {farmer.username}")
    
    # Create sample buyer
    if not User.objects.filter(username='buyer1').exists():
        buyer = User.objects.create_user(
            username='buyer1',
            email='buyer@example.com',
            password='testpass123',
            full_name='Jane Buyer',
            phone_number='+0987654321',
            user_type='Buyer'
        )
        print(f"✅ Created buyer: {buyer.username}")
    
    print("\n🔑 Sample login credentials:")
    print("Farmer - Username: farmer1, Password: testpass123")
    print("Buyer - Username: buyer1, Password: testpass123")

if __name__ == '__main__':
    setup_database()
