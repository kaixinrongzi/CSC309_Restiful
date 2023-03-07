from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, DeleteView, UpdateView, DetailView
from .forms import LoginForm, RegisterForm, ProfileForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class UserRegister(CreateView):
    # fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
    # fields ='__all__'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'register.html'

    # note that ModelForm saves object automatically
    def form_valid(self, form):
        # self.request.session['from'] = 'register'

        return super().form_valid(form)


class UserLogin(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy("accounts:viewprofile")

    def form_valid(self, form):
        print("login form is valid")
        user = form.cleaned_data['user']
        print(user)
        self.request.session['user'] = user.pk
        login(self.request, user)
        return super().form_valid(form)






# def UserLogout(request):
#     # request.session['from'] = form.cleaned_data['user']
#     logout(request)
#     return redirect(reverse_lazy('login'))


class UserLogout(View):
    success_url = reverse_lazy("accounts:login")

    def get(self, request):
        logout(request)
        # return redirect(self.success_url)
        return HttpResponseRedirect(self.success_url, status=302)


# def UserProfile(request):
#     user_id = request.session['user']
#     print(user_id)
#     user = User.objects.get(id=user_id)
#     return JsonResponse({'id': user.id,
#                          "username": user.username,
#                          "email": user.email,
#                          "first_name": user.first_name,
#                          "last_name": user.last_name})


# class ProductViewMixin(LoginRequiredMixin):      # only authenticated user is allowed to do what????
#     form_class = ProductForm
#     login_url = reverse_lazy('accounts:login')
#     success_url = reverse_lazy('stores:home')
#     template_name = "stores/inventory.html"
#
#     def get_context_data(self, **kwargs):        # the function is called when web browser is going to render inventory.html
#         context = super().get_context_data(**kwargs)
#         context['store'] = self.request.user.store
#         return context


class UserProfileView(FormView):
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("accounts:viewprofile")
    # login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("64")
        print("66")
        user = self.request.user
        print("user logined: ", self.request.user.is_authenticated)
        json_response = {'id': user.id,
                         "username": user.username,
                         "email": user.email,
                         "first_name": user.first_name,
                         "last_name": user.last_name}
        context['user_json'] = json_response
        context['link'] = 'view'
        context['user'] = user
        print("view")
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        else:
            context = {}
            json_response = {'id': user.id,
                             "username": user.username,
                             "email": user.email,
                             "first_name": user.first_name,
                             "last_name": user.last_name}
            context['user_json'] = json_response
            context['link'] = 'view'
            context['user'] = user
            print("view")
            return render(request, self.template_name, context)


class UserProfileEdit2(UserProfileView, UpdateView):
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user)
        context['user'] = user
        context['link'] = 'edit'
        return context

    def form_valid(self, form):
        user = form.save()
        new_password = form.cleaned_data["password1"]
        if new_password != "":
            user.set_password(new_password)
            user.save()
            login(self.request, user)
        else:
            user.save()
        return redirect(self.success_url)


class UserProfileEdit(FormView):
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("accounts:viewprofile")
    # login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        print("123")
        return User.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        print("127")
        # user_id = self.request.session['user']
        # user = User.objects.get(id=user_id)
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # form = self.form_class({"first_name": user.first_name,
        #                         "last_name": user.last_name,
        #                         "email": user.email})
        context['user'] = user
        # context['form'] = form
        context['link'] = 'edit'
        return context

    def form_valid(self, form):
        user = self.request.user
        print("user logined: ", self.request.user.is_authenticated)
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]
        new_password = form.cleaned_data["password1"]
        # user.save()
        print("147")
        if new_password != "":
            user.set_password(new_password)
            user.save()
            login(self.request, user)
            print("150")
        else:
            user.save()
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        print(user)
        form = self.form_class({"first_name": user.first_name,
                                "last_name": user.last_name,
                                "email": user.email})
        context = {'form': form,
                   'user': user,
                   'link': 'edit'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        return super().post(request, *args, **kwargs)


    # def get_queryset(self):
    #     # user_id = self.request.session['user']
    #     # user = User.objects.get(id=user_id)
    #     # print("get_queryset", user)
    #     # return user
    #     print("lalala")
    #     return User.objects.filter(id=self.request.user.id)  # self.request is a form

    # class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()
#
#     def get_object(self):
#         return get_object_or_404(Item, id=self.kwargs['pk'])   # the first field of Item is "id"
