from django.forms import ModelForm
from ecom.models import Address

class AddressCheckoutForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"