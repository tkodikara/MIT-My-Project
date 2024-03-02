from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views import View

from .forms import WarehouseForm, ShipmentItemForm
from .models import Product, QCStock, TransferNote, WarehouseStock, Shipment, ShipmentItem, GatePass


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
        product_count = Product.objects.all().count()
        ware_house_stock = WarehouseStock.objects.aggregate(total_count=Sum('quantity'))
        intransist_stock = TransferNote.objects.aggregate(total_count=Sum('quantity'))
        qc_stock = QCStock.objects.aggregate(total_count=Sum('quantity'))
        context = {
            "title": "Dashboard - Warehouse Management System",
            "product_count": product_count,
            "ware_house_stock_on_hand": ware_house_stock['total_count'] or 0,
            "intransist_stock": intransist_stock['total_count'] or 0,
            "qc_stock": qc_stock['total_count'] or 0,
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


class ShipmentCreateView(CreateView):
    model = Shipment
    template_name = 'products/shipment_create.html'
    success_url = reverse_lazy('products:warehouse-stock')
    fields = ['shipment_number']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create Shipment - Warehouse Management System"
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:shipment-update', kwargs={'pk': self.object.pk})


class ShipmentUpdate(UpdateView):
    model = Shipment
    template_name = 'products/shipment_update.html'
    fields = ['shipment_number']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Shipment - Warehouse Management System"
        context['warehouse_stock'] = WarehouseStock.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('products:shipment-item-update', kwargs={'pk': self.object.shipment.pk})


class ShimpentItemCreateView(CreateView):
    model = ShipmentItem
    template_name = 'products/shipment_update.html'
    form_class = ShipmentItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Shipment - Warehouse Management System"
        context['warehouse_stock'] = WarehouseStock.objects.all()
        return context

    def form_valid(self, form):
        form.instance.warehousestock.quantity -= form.instance.quantity
        form.instance.warehousestock.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:shipment-update', kwargs={'pk': self.object.shipment.pk})

    def form_invalid(self, form):
        return redirect(reverse_lazy('products:shipment-update', kwargs={'pk': form.instance.shipment.pk}))


class ShipmentListView(ListView):
    model = Shipment
    template_name = 'products/shipment_list.html'
    context_object_name = 'shipment_list'
    paginate_by = 10
    queryset = Shipment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Shipment List - Warehouse Management System"
        return context


class ShipmentDetailView(DetailView):
    template_name = 'products/shipment_detail.html'
    model = Shipment
    context_object_name = 'shipment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Shipment Detail - Warehouse Management System"
        return context


class GatePassCreateView(CreateView):
    model = GatePass
    template_name = 'products/gatepass.html'
    fields = ['container_number']

    def form_valid(self, form):
        form.instance.shipment = Shipment.objects.get(pk=self.request.GET.get('shipment_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:shipment-detail', kwargs={'pk': self.object.shipment.pk})
