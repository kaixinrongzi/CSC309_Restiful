from django.forms import ModelForm, Form
from banks.models import Bank


class BankAddForm(ModelForm):
    class Meta:
        model = Bank
        exclude = ('owner',)