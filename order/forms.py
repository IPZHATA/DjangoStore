from django import forms
from .models import DeliveryProvider

class OrderForm(forms.Form):
    delivery_option = forms.ModelChoiceField(
        queryset=DeliveryProvider.objects.all(),
        widget=forms.RadioSelect
    )
    # payment_option = forms.ModelChoiceField(
    #     queryset=PaymentOption.objects.all(),
    #     widget=forms.RadioSelect
    # )


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=19,
                                  label='Номер картки',
                                  widget=forms.TextInput(attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX', 'pattern': '[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}'}))
    expiry_date = forms.CharField(max_length=5,
                                  label='Дійсна до',
                                  widget=forms.TextInput(attrs={'placeholder': 'XX/XX', 'pattern': '[0-9]{2}/[0-9]{2}'}))
    cvv = forms.CharField(max_length=3,
                          label='CVV',
                          widget=forms.TextInput(attrs={'placeholder': 'XXX', 'pattern': '[0-9]{3}'}))