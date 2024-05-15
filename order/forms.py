from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

        help_texts = {
            'house': 'інформація про дім (номер поверху, під\'їзу)'
        }

        labels = {
            'house': 'Будинок',
            'zip_code': 'Поштовий індекс',
            'state': 'Область',
            'city': 'Місто',
            'street': 'Вулиця',
        }


class PaymentForm(forms.Form):
    def __init__(self, *args, order=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order

    card_number = forms.CharField(max_length=19,
                                  label='Номер картки',
                                  widget=forms.TextInput(attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX',
                                                                'pattern': '[0-9]{4}-?[0-9]{4}-?[0-9]{4}-?[0-9]{4}'}))
    expiry_date = forms.CharField(max_length=5,
                                  label='Дійсна до',
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'XX/XX', 'pattern': '[0-9]{2}/[0-9]{2}'}))
    cvv = forms.CharField(max_length=3,
                          label='CVV',
                          widget=forms.TextInput(attrs={'placeholder': 'XXX', 'pattern': '[0-9]{3}'}))
    error_messages = {
        'card_number': {
            'required': 'Це поле є обов\'язковим'
        },
        'expiry_date': {
            'required': 'Це поле є обов\'язковим'
        },
        'cvv': {
            'required': 'Це поле є обов\'язковим'
        }
    }
