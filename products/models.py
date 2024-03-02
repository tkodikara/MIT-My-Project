# Create your models here.

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    class ProductStates(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    product_code = models.IntegerField()
    product_description = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_weight = models.FloatField()
    product_volume = models.FloatField()
    barcode = models.ImageField(upload_to="qr_code_img/", blank=True, null=True)
    states = models.CharField(
        max_length=10,
        choices=ProductStates,
        default=ProductStates.ACTIVE,
    )

    def __str__(self):
        return f"{self.product_description}"


class QCStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    def add_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")
        self.quantity += quantity
        self.save()

    def remove_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")
        self.quantity -= quantity
        self.save()

    def get_update_url(self):
        return reverse('products:update-qc-stock', kwargs={'pk': self.pk})


class TransferNote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    transferred_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    def add_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")
        self.quantity += quantity
        self.save()

    def remove_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")
        self.quantity -= quantity
        self.save()


class AllocatedLocation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def add_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > self.max_quantity:
            raise ValueError("Quantity cannot be greater than the maximum quantity")
        if quantity + self.quantity > self.max_quantity:
            raise ValueError("Available Quantity is not enough to accommodate the quantity")
        self.quantity += quantity
        self.save()

    def remove_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")
        self.available_quantity -= quantity
        self.save()


class WarehouseStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    location = models.ForeignKey(AllocatedLocation, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_description}"
