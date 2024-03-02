from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views import View

from .forms import WarehouseForm
from .models import Product, QCStock, TransferNote, WarehouseStock


@login_required
def detail(request):
    products = Product.objects.all()
    context = {
        "products": products,
        "title": "Product List - Warehouse Management System"
    }
    return render(request, "products/products.html", context)


@login_required
def scan_stock(request):
    qc_stocks = QCStock.objects.all()
    context = {
        "qc_stocks": qc_stocks,
        "title": "Product List - Warehouse Management System"
    }
    return render(request, "products/scan_stock.html", context)


class ProductCreateView(LoginRequiredMixin, CreateView):
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


class UpdateQCStockView(LoginRequiredMixin, UpdateView):
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


class QCStockListView(LoginRequiredMixin, ListView):
    model = QCStock
    template_name = 'products/qc_stock_list.html'
    context_object_name = 'qc_stocks'
    paginate_by = 10
    queryset = QCStock.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "QC Stock List - Warehouse Management System"
        return context


class CreateTransferNoteView(LoginRequiredMixin, CreateView):
    model = TransferNote
    template_name = 'products/create_transfer_note.html'
    fields = ['quantity']
    success_url = reverse_lazy('products:transfer-list')

    def get_qc_stock(self):
        return QCStock.objects.get(pk=self.request.GET.get('qc_stock_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_qc_stock().product
        context['title'] = "Create Transfer Note - Warehouse Management System"
        context['product'] = product
        return context

    def form_valid(self, form):
        qc_stock = self.get_qc_stock()
        product = qc_stock.product
        form.instance.product = product
        form.instance.transferred_by = self.request.user
        qc_stock.remove_quantity(form.instance.quantity)
        return super().form_valid(form)


class HomePage(LoginRequiredMixin, View):
    template_name = "products/home_page.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Dashboard - Warehouse Management System"
        }
        return render(request, self.template_name, context)


class TransferListView(LoginRequiredMixin, ListView):
    model = TransferNote
    template_name = 'products/transfer_list.html'
    context_object_name = 'transfer_notes'
    paginate_by = 10
    queryset = TransferNote.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "In Transit List - Warehouse Management System"
        return context


class WareHouseStockListView(LoginRequiredMixin, ListView):
    model = WarehouseStock
    template_name = 'products/warehousestock_list.html'
    context_object_name = 'warehouse_stock'

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Warehouse Stock List - Warehouse Management System"
        return context


class WareHouseCreateView(CreateView):
    model = WarehouseStock
    template_name = 'products/warehouse_create.html'
    success_url = reverse_lazy('products:warehouse-stock')
    form_class = WarehouseForm

    def get_transist_stock(self):
        transist_stock = TransferNote.objects.get(pk=self.request.GET.get('transist_stock_id'))
        return transist_stock

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['transist_stock'] = self.get_transist_stock()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transist_stock = self.get_transist_stock()
        context['title'] = "Create Warehouse Stock - Warehouse Management System"
        context['transist_stock'] = transist_stock
        context['product'] = transist_stock.product
        return context

    def form_valid(self, form):
        transist_stock = self.get_transist_stock()
        product = transist_stock.product
        form.instance.product = product
        form.instance.accepted_by = self.request.user
        transist_stock.remove_quantity(form.instance.quantity)
        form.instance.location.quantity += form.instance.quantity
        form.instance.location.save()
        return super().form_valid(form)
