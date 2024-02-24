import os

from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver

from .helpers import generate_qr_image
from .models import Product, QCStock


@receiver(post_save, sender=Product)
def create_profile(sender, instance, created, **kwargs):
    """Signal to create a QCStock instance when a Product is created."""
    if created:
        # Create a QCStock instance for the product
        qc_stock = QCStock.objects.create(product=instance)
        url = qc_stock.get_update_url()
        image_name = f"qc_stock_{instance.product_code}.png"
        generate_qr_image(
            url,
            image_name
        )
        with open(image_name, "rb") as f:
            # Save the QR code image to the product
            instance.barcode = File(f)
            instance.save()
        os.remove(image_name)


