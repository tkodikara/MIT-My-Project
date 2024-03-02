from django.core.exceptions import ValidationError
from django.forms import ModelForm

from products.models import WarehouseStock, AllocatedLocation


class WarehouseForm(ModelForm):
    class Meta:
        model = WarehouseStock
        fields = ['quantity', 'location']

    def __init__(self, *args, **kwargs):
        self.transist_stock = kwargs.pop('transist_stock', None)
        super().__init__(*args, **kwargs)

    def clean_location(self):
        location: AllocatedLocation = self.cleaned_data.get('location')
        quantity = self.cleaned_data.get('quantity')
        if self.transist_stock.quantity < quantity:
            raise ValidationError("Quantity cannot be greater than transist stock")
        if location.max_quantity < quantity:
            raise ValidationError("Quantity cannot be greater than max stock")
        if location.quantity + quantity > location.max_quantity:
            raise ValidationError(f"Only {location.max_quantity - location.quantity} units "
                                  f"can be added to the location. "
                                  f"current stock is {location.quantity} and max stock is "
                                  f"{location.max_quantity}")
        return location
