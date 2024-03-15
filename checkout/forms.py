from django import forms
from .models import Order


# model for the order form
class OrderForm(forms.ModelForm):
    class Meta:
        # uses the Order model
        model = Order
        # Show fields that will need to be completed
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # Set up default form
        super().__init__(*args, **kwargs)
        # Placeholders dictionary
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Set cursor to focus on Full Name field when form loaded
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # Iterate through form fields
        for field in self.fields:
            if field != "country":
                # If it's a required field add a *
                # Add placeholder text to each field
                # Remove label from each field
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
