from django.urls import path, include
from .views import BankAddView, BankView, BankViewAll, BranchAddView, BranchView, BranchViewAll, BranchEdit

app_name="banks"
urlpatterns = [
    path('add/', BankAddView.as_view(), name="addbank"),    # both get + post; get: template_name, post: form_valid
    path('<bank_id>/details/', BankView.as_view(), name="bankview"),
    path("all/", BankViewAll.as_view(), name="bankviewall"),
    path('<bank_id>/branches/add/', BranchAddView.as_view(), name="addbranch"),
    path("branch/<branch_id>/details/", BranchView.as_view(), name="branchview"),
    path('<bank_id>/branches/all/', BranchViewAll.as_view(), name="branchviewall"),
    path("branch/<int:pk>/edit/", BranchEdit.as_view(), name="branchedit")
]