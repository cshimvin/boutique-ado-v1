from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # check if there is a size
    if size:
        if item_id in list(bag.keys()):
            # if an item of that size already exists,
            # increase quantity by 1
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # otherwise if item is in the bag but a new size
                # has been added, add the item with the new size
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # If a new item is added with a size, add to bag
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # if item doesn't have a size, add to bag without size
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
