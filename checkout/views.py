from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    # get the bag session content or empty if doesn't exist
    bag = request.session.get('bag', {})
    # if nothing is in the bag, display message
    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51OtqHjBRHMXsOWRLrchPAiPXbxwxgOy1TIUodgKxfH02osx29JCP4O78Mv2fKAIJNUu9Xl458zsWsyO0zpOyzkaE00pGFSi6vc',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
