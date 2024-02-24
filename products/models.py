# Create your models here.

from django.db import models


class Product(models.Model):
    class ProductStates(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    product_code = models.IntegerField()
    product_description = models.CharField(max_length=60)
    product_category = models.CharField(max_length=30)
    product_weight = models.FloatField()
    product_volume = models.FloatField()
    barcode_ID = models.FloatField()
    warehouse_number = models.FloatField()
    states = models.CharField(
        max_length=10,
        choices=ProductStates,
        default=ProductStates.ACTIVE,
    )


class QCStockItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_description = models.CharField(max_length=60)
    quantity = models.IntegerField()


class TransferNote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transferred_by = models.CharField(max_length=255)


class AllocatedLocation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()


class WarehouseStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_description = models.CharField(max_length=60)
    quantity = models.IntegerField()
    location = models.ForeignKey(AllocatedLocation, on_delete=models.CASCADE)
    accepted_by = models.CharField(max_length=255)
