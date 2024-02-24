from django.contrib import admin
from .models import Product, QCStockItem, TransferNote, AllocatedLocation, WarehouseStock
# Register your models here.
admin.site.register(Product)
admin.site.register(QCStockItem)
admin.site.register(TransferNote)
admin.site.register(AllocatedLocation)
admin.site.register(WarehouseStock)
