from django.shortcuts import render, get_object_or_404, redirect, reverse
# Enable Django to display messages
from django.contrib import messages
# Import query library for search form
from django.db.models import Q
from .models import Product
# Create your views here.


def all_products(request):
    """
    View to show all products, including sorting and search queries
    """
    # Get all products
    products = Product.objects.all()
    # Set search term to None to prevent errors
    query = None

    # Check if GET action performed
    if request.GET:
        # Check if there was a search term entered
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
