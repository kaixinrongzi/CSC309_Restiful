from django.forms import ModelForm, Form
from ..models import Bank


class BankAddForm(ModelForm):
    class Meta:
        model = Bank
        exclude = ('owner',)


class BankViewForm(ModelForm):
    class Meta:
        model = Bank
        exclude = ('owner',)


class BankViewAllForm(ModelForm):
    class Meta:
        model = Bank
        exclude = ('owner',)