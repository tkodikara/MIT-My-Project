from django.contrib import admin
from .models import Product, QCStock, TransferNote, AllocatedLocation, WarehouseStock, Category
# Register your models here.
admin.site.register(Product)
admin.site.register(QCStock)
admin.site.register(TransferNote)
admin.site.register(AllocatedLocation)
admin.site.register(WarehouseStock)
admin.site.register(Category)
