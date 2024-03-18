from django.shortcuts import render, get_object_or_404, redirect, reverse
# Enable Django to display messages
from django.contrib import messages
# Import query library for search form
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """
    View to show all products, including sorting and search queries
    """
    # Get all products
    products = Product.objects.all()
    # Set search term and category to None to prevent errors
    query = None
    categories = None
    sort = None
    direction = None

    # Check if GET action performed
    if request.GET:
        # Check if sort has been requested
        if 'sort' in request.GET:
            # Create a key to sort on
            sortkey = request.GET['sort']
            # Preserve the original request
            sort = sortkey
            if sortkey == "name":
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == "desc":
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

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

    current_sorting = f'{sort}_{direction}'

    context = {
        "products": products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting
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


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. \
                           Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. \
                           Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def delete_product(request, product_id):
    """ Delete a product from the store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
