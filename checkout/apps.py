from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    # override the default ready method with one that listens to signals
    def ready(self):
        import checkout.signals
