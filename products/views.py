from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from .models import Product, QCStock


def detail(request):
    products = Product.objects.all()
    context = {
        "products": products,
        "title": "Product List - Warehouse Management System"
    }
    return render(request, "products/products.html", context)


class ProductCreateView(CreateView):
    model = Product
    fields = [
        'product_code',
        'product_description',
        'product_category',
        'product_weight',
        'product_volume',
        'barcode',
        'states'
    ]
    template_name = 'products/add_product.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create Product - Warehouse Management System"
        return context


class UpdateQCStockView(UpdateView):
    model = QCStock
    fields = ['quantity']
    template_name = 'products/update_qc_stock.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qc_stock = self.get_object()
        context['title'] = "Update QC - Warehouse Management System"
        context['qc_stock'] = qc_stock
        context['product'] = qc_stock.product
        return context

    def get_success_url(self):
        return self.get_object().get_update_url()
