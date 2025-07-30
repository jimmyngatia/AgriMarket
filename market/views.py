from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProductForm
from .models import User, Product
from django.db.models import Q

def home(request):
    """Home page view with featured products"""
    # Get only the 3 most recent products for the homepage
    featured_products = Product.objects.all().select_related('farmer').order_by('-created_at')[:3]
    
    # Get total product count for display
    total_products = Product.objects.count()
    
    context = {
        'featured_products': featured_products,
        'total_products': total_products,
    }
    
    return render(request, 'market/home.html', context)

def products_list(request):
    """All products page with search and filter functionality"""
    products = Product.objects.all().select_related('farmer')
    
    # Get filter parameters from request
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    location_filter = request.GET.get('location', '')
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(farmer__full_name__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter:
        products = products.filter(category=category_filter)
    
    # Apply price range filters
    if min_price:
        try:
            min_price_val = float(min_price)
            products = products.filter(price__gte=min_price_val)
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price_val = float(max_price)
            products = products.filter(price__lte=max_price_val)
        except ValueError:
            pass
    
    # Apply location filter
    if location_filter:
        products = products.filter(location__icontains=location_filter)
    
    # Order by most recent
    products = products.order_by('-created_at')
    
    # Get all categories for the filter dropdown
    categories = Product.CATEGORY_CHOICES
    
    # Get unique locations for suggestions (optional)
    locations = Product.objects.values_list('location', flat=True).distinct()[:10]
    
    context = {
        'products': products,
        'categories': categories,
        'locations': locations,
        'search_query': search_query,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'location_filter': location_filter,
        'total_products': products.count(),
    }
    
    return render(request, 'market/products_list.html', context)


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Log the user in after registration
            login(request, user)
            
            # Redirect based on user type
            if user.user_type == 'Farmer':
                return redirect('dashboard')
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """Custom login view with redirect logic"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name or user.username}!')
                
                # Redirect based on user type
                if user.user_type == 'Farmer':
                    return redirect('dashboard')
                else:
                    return redirect('home')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard view for farmers"""
    if request.user.user_type != 'Farmer':
        messages.warning(request, 'Access denied. This page is for farmers only.')
        return redirect('home')
    
    # Get all products for the current farmer
    products = Product.objects.filter(farmer=request.user)
    
    # Calculate stats
    total_products = products.count()
    total_value = sum(product.price * product.quantity for product in products)
    
    context = {
        'products': products,
        'total_products': total_products,
        'total_value': total_value,
    }
    
    return render(request, 'market/dashboard.html', context)


@login_required
def add_product(request):
    """Add new product view for farmers"""
    if request.user.user_type != 'Farmer':
        messages.warning(request, 'Access denied. Only farmers can add products.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" has been added successfully!')
            return redirect('dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'market/add_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    """Delete product view for farmers"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the current user is the owner of the product
    if product.farmer != request.user:
        messages.error(request, 'You can only delete your own products.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'market/delete_product.html', {'product': product})


def profile_view(request):
    """User profile view"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'market/profile.html')

def product_detail(request, product_id):
    """Product detail view"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get other products from the same farmer
    other_products = Product.objects.filter(farmer=product.farmer).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'other_products': other_products,
    }
    
    return render(request, 'market/product_detail.html', context)
