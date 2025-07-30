from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product


class CustomUserAdmin(UserAdmin):
    # Add the custom fields to the admin interface
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('full_name', 'phone_number', 'user_type')
        }),
    )
    
    # Add custom fields to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('full_name', 'phone_number', 'user_type')
        }),
    )
    
    # Display these fields in the user list
    list_display = ['username', 'email', 'full_name', 'user_type', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_superuser']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'category', 'price', 'quantity', 'location', 'created_at']
    list_filter = ['category', 'created_at', 'farmer__user_type']
    search_fields = ['name', 'farmer__username', 'farmer__full_name', 'location']
    readonly_fields = ['created_at']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
