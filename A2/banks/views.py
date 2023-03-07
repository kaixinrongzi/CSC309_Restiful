from django.views.generic import CreateView, FormView, DeleteView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms.BankAddForm import BankAddForm, BankViewForm, BankViewAllForm
from .forms.BranchAddForm import BranchAddForm, BranchEditForm, BranchViewForm, BranchViewAllForm
from .models import Bank, Branch


class BankAddView(LoginRequiredMixin, FormView):
    form_class = BankAddForm
    template_name = "create.html"
    success_url = reverse_lazy("banks:bankview")
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):  # called by both get & post method
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context

    # called by post method: form_valid(self, form)
    def form_valid(self, form):
        bank = form.save()
        bank.owner = self.request.user
        bank.save()
        bank_id = bank.id
        return redirect(reverse(viewname="banks:bankview", kwargs={"bank_id": bank_id}))


class BankView(DetailView):
    form_class = BankViewForm
    template_name = "create.html"

    def get(self, request, *args, **kwargs):
        full_path = request.get_full_path()
        full_path_lst = full_path.split("/")
        bank_id = full_path_lst[-3]
        bank = Bank.objects.filter(pk=bank_id).first()
        if bank is None:
            return HttpResponse(status=404)
        response = "<h1>{0}</h1><p>Swift Code: {1}</p><p>Institution Number: {2}</p><p>Bank Description: {3}</p>".format(
            bank.name, bank.swift_code, bank.inst_num, bank.description)
        return HttpResponse(response)

    # def get_queryset(self):
    #     full_path = self.request.get_full_path()
    #     full_path_lst = full_path.split("/")
    #     bank_id = full_path_lst[-3]
    #     # bank = Bank.objects.get(pk=bank_id)
    #     return Bank.objects.filter(pk=bank_id)


class BankViewAll(ListView):
    # model = Bank
    template_name = "list.html"
    form_class = BankViewAllForm

    def get_queryset(self):
        # user = self.request.user
        banks = Bank.objects.all()
        return banks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_banks = Bank.objects.all()
        context["banks"] = all_banks
        return context

    # def get(self, request, *args, **kwargs):
    #     all_banks = Bank.objects.all()
    #     banks_info = "<ol>"
    #     for bank in all_banks:
    #         bank_id = bank.id
    #         bank_name = bank.name
    #         bank_info = "<li>id: {0}, name: {1}</li>".format(bank_id, bank_name)
    #         banks_info = banks_info + bank_info
    #     banks_info = banks_info + "</ol>"
    #     return HttpResponse(banks_info)


        # response = "<h1>{0}</h1><p>Swift Code: {1}</p><p>Institution Number: {2}</p><p>Bank Description: {3}</p>".format(
        #     bank.name, bank.swift_code, bank.inst_num, bank.description)
        # return HttpResponse(response)


class BranchAddView(LoginRequiredMixin, FormView):
    form_class = BranchAddForm
    template_name = "branch.html"
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy("banks:branchview")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # context contains form
        user = self.request.user
        context["user"] = user
        context['link'] = "create"
        return context

    def form_valid(self, form):
        full_path = self.request.get_full_path()
        full_path_lst = full_path.split("/")
        bank_id = int(full_path_lst[-4])
        bank = Bank.objects.get(pk=bank_id)
        branch = form.save()
        branch.bank = bank
        branch.save()
        return redirect(reverse("banks:branchview", kwargs={"branch_id": branch.pk}))

    def get(self, request, *args, **kwargs):
        full_path = request.get_full_path()
        full_path_lst = full_path.split("/")
        bank_id = full_path_lst[-4]
        bank = Bank.objects.filter(pk=bank_id).first()
        # if the bank DNE
        if bank is None:
            return HttpResponse(status=404)
        user = request.user
        if bank.owner.pk != user.pk:
            return HttpResponse(status=403)
        form = self.form_class()
        context = {"user": user, "link": "create", 'form': form}
        return render(request, self.template_name, context)


class BranchView(DetailView):
    form_class = BranchViewForm
    template_name = "branch.html"

    def get(self, request, *args, **kwargs):
        full_path = request.get_full_path()
        full_path_lst = full_path.split("/")
        branch_id = full_path_lst[-3]
        branch = Branch.objects.filter(pk=branch_id).first()
        if branch is None:
            return HttpResponse(status=404)
        jsresponse = {"id": branch.id,
                      "name": branch.name,
                      "transit_num": branch.transit_num,
                      "address": branch.address,
                      "email": branch.email,
                      "capacity": branch.capacity,
                      "last_modified": branch.last_modified}
        return JsonResponse(jsresponse)


class BranchViewAll(DetailView):
    form_class = BranchViewAllForm

    def get(self, request, *args, **kwargs):
        full_path = request.get_full_path()
        full_path_lst = full_path.split("/")
        bank_id = full_path_lst[-4]
        my_bank = Bank.objects.filter(pk=bank_id).first()
        if my_bank is None:
            return HttpResponse(status=404)
        branches = Branch.objects.filter(bank=my_bank)

        jsresponse = []
        for branch in branches:
            jsresponse.append({"id": branch.id,
                               "name": branch.name,
                               "transit_num": branch.transit_num,
                               "address": branch.address,
                               "email": branch.email,
                               "capacity": branch.capacity,
                               "last_modified": branch.last_modified})
        # return JsonResponse(jsresponse)
        return JsonResponse(jsresponse, safe=False)


class BranchEdit(UpdateView):
    form_class = BranchEditForm
    template_name = "edit_branch.html"
    success_url = reverse_lazy("banks:branchview")

    def get_queryset(self):     # called whenever get or post, but called after get
        print("get_queryset")
        user = self.request.user
        if not user.is_authenticated:
            return HttpResponse(status=401)
        full_path = self.request.get_full_path()
        full_path_lst = full_path.split("/")
        branch_id = full_path_lst[-3]
        print("branch_id:", branch_id)
        return Branch.objects.filter(pk=branch_id)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)  # context contains form
    #     user = self.request.user
    #     branch = self.get_queryset().first()
    #     print("163")
    #     form = self.form_class({"name": branch.name,
    #                             "transit_num": branch.transit_num,
    #                             "address": branch.address,
    #                             "email": branch.email,
    #                             "capacity": branch.capacity})
    #     context["form"] = form
    #     context["user"] = user
    #     context['link'] = "edit"
    #     return context

    def form_valid(self, form):
        branch = form.save()
        branch.last_modified = form.cleaned_data["last_modified"]
        branch.save()
        return redirect(reverse("banks:branchview", kwargs={"branch_id": branch.id}))

    def get(self, request, *args, **kwargs):
        print("get")
        user = self.request.user
        if not user.is_authenticated:
            return HttpResponse(status=401)
        full_path = request.get_full_path()
        full_path_lst = full_path.split("/")
        branch_id = full_path_lst[-3]
        branch = Branch.objects.filter(pk=branch_id).first()
        if branch is None:
            return HttpResponse(status=404)
        user = request.user
        if branch.bank.owner.pk != user.pk:
            return HttpResponse(status=403)

        # context = {}
        # form = self.form_class({"name": branch.name,
        #                         "transit_num": branch.transit_num,
        #                         "address": branch.address,
        #                         "email": branch.email,
        #                         "capacity": branch.capacity})
        # context["form"] = form
        # context["user"] = user
        # context['link'] = "edit"
        return super().get(request, *args, **kwargs)
        # return render(request, self.template_name, context)






