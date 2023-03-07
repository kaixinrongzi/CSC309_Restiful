from django.forms import ModelForm, Form
from ..models import Branch
from django.utils import timezone


class BranchAddForm(ModelForm):
    class Meta:
        model = Branch
        exclude = ('bank',)

    # def clean(self):     # called by both GET and POST
    #     cleaned = super().clean()
    #     bank = cleaned.get("bank")
    #     url_full_path = self.request.get_full_path()
    #     url_full_path_lst = url_full_path.split("")
    #     bank_id = url_full_path_lst[-6]
    #     if bank.id != bank_id:
    #         raise ValidationError("wrong bank")
    #     cleaned["branch"] = cleaned
    #     return cleaned


class BranchEditForm(ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "transit_num", "address", "email", "capacity"]

    def clean(self):
        cleaned = super().clean()
        cleaned["last_modified"] = timezone.now()
        cleaned["branch"] = cleaned
        return cleaned


class BranchViewForm(ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "transit_num", "address", "email", "capacity"]


class BranchViewAllForm(ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "transit_num", "address", "email", "capacity"]




