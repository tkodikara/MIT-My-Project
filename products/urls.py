from django.urls import path

from .views import detail, ProductCreateView, UpdateQCStockView, QCStockListView, CreateTransferNoteView

app_name = 'products'
urlpatterns = [
    path('', detail, name='home'),
    path('add-product/', ProductCreateView.as_view(), name='add-product'),
    path('qc-stock/<int:pk>/update/', UpdateQCStockView.as_view(), name='update-qc-stock'),
    path('qc-stock/', QCStockListView.as_view(), name='qc-stock-list'),
    path('create-transfer-note/', CreateTransferNoteView.as_view(), name='create-transfer-note'),

]
