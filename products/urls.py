from django.urls import path

from .views import detail, ProductCreateView, UpdateQCStockView

app_name = 'products'
urlpatterns = [
    path('', detail, name='home'),
    path('add-product/', ProductCreateView.as_view(), name='add-product'),
    path('qc-stock/<pk>/update/', UpdateQCStockView.as_view(), name='update-qc-stock'),
]