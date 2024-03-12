# Signals are used to update the totals after order items are saved
# or deleted

# Send signal when saved or deleted
from django.db.models.signals import post_save, post_delete
# Receive sent signal
from django.dispatch import receiver

# import line item model which is where we'll listen for signals
from .models import OrderLineItem


# Updates the order model sender = OrderLineItem,
# instance of the model that sent it, if it's a new instance
# or one being updated and any keyword arguments
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    # Use the update_total method from the Order model
    instance.order.update_total()


# Updates the order model when a line item is deleted
@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    # Use the update_total method from the Order model
    instance.order.update_total()
