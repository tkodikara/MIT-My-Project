from django.urls import path

from .views import (detail, ProductCreateView, UpdateQCStockView, QCStockListView,
                    CreateTransferNoteView, HomePage, TransferListView, scan_stock,
                    WareHouseStockListView)

app_name = 'products'
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('products/', detail, name='product'),
    path('scan_stock/', scan_stock, name='scan_stock'),
    path('add-product/', ProductCreateView.as_view(), name='add-product'),
    path('qc-stock/<int:pk>/update/', UpdateQCStockView.as_view(), name='update-qc-stock'),
    path('qc-stock/', QCStockListView.as_view(), name='qc-stock-list'),
    path('create-transfer-note/', CreateTransferNoteView.as_view(), name='create-transfer-note'),
    path('transfer-list/', TransferListView.as_view(), name='transfer-list'),
    path('warehouse-stock/', WareHouseStockListView.as_view(), name='warehouse-stock'),
]
