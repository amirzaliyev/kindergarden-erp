from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from .forms import UserAuthForm

# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "authentication/index.html"


class UserRegisterView(TemplateView):
    template_name = "authentication/register.html"


class AuthenticationView(LoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True
    redirect_field_name = "next"
    form_class = UserAuthForm

    def form_valid(self, form):
        remember_me = form.cleaned_data["remember_me"]
        user = form.get_user()

        login(self.request, user)

        if remember_me is False:
            self.request.session.set_expiry(0)

        return super().form_valid(form)

    def form_invalid(self, form):
        for err in form.errors["__all__"]:
            messages.error(self.request, err)

        return super().form_invalid(form)
