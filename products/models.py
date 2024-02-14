from django.db import models

# Create your models here.


class Category(models.Model):
    """ Categories model for the database """
    name = models.CharField(max_length=254)
    # This is a displayable name on the website
    # null=True and blank=True means it's optional
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    # method to return the name of the category
    def __str__(self):
        return self.name

    # method to return the friendly name of the category
    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """ Products model for the database """
    # Category taken from the categories table. Can be optional. If it
    # is deleted, then set the category to NULL instead of deleting all
    # products for that category
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
