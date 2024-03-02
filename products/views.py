from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views import View

from .models import Product, QCStock, TransferNote


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
        return reverse_lazy('products:qc-stock-list')


class QCStockListView(ListView):
    model = QCStock
    template_name = 'products/qc_stock_list.html'
    context_object_name = 'qc_stocks'
    paginate_by = 10
    queryset = QCStock.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "QC Stock List - Warehouse Management System"
        return context


class CreateTransferNoteView(CreateView):
    model = TransferNote
    template_name = 'products/create_transfer_note.html'
    fields = ['quantity']
    success_url = reverse_lazy('products:qc-stock-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.request.GET.get('product_id'))
        context['title'] = "Create Transfer Note - Warehouse Management System"
        context['product'] = product
        return context


class HomePage(View):
    template_name = "form_template.html"
