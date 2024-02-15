from django.shortcuts import render, get_object_or_404, redirect, reverse
# Enable Django to display messages
from django.contrib import messages
# Import query library for search form
from django.db.models import Q
from .models import Product, Category
# Create your views here.


def all_products(request):
    """
    View to show all products, including sorting and search queries
    """
    # Get all products
    products = Product.objects.all()
    # Set search term and category to None to prevent errors
    query = None
    categories = None

    # Check if GET action performed
    if request.GET:
        # Check if a specific category was selected
        if 'category' in request.GET:
            # If more than one category in the comma-separated list, then
            # split the list
            categories = request.GET['category'].split(',')
            # Filter products according to categories
            products = products.filter(category__name__in=categories)
            # Get category names according to the filter
            categories = Category.objects.filter(name__in=categories)

        # Check if there was a search term entered
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                # Create an error message to be displayed on the page
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            # As a standard search searches both product name AND description,
            # use Q function imported above to search OR. The i in the query
            # means it is a case insensitive search.
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # Filter products based on the query
            products = products.filter(queries)

    context = {
        "products": products,
        'search_term': query,
        'current_categories': categories,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """
    View to show product details based on product_id
    """
    # Get product with a specific product ID
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    return render(request, "products/product_detail.html", context)
