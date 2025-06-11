from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView

from .forms import UserLoginModel

# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "web/index.html"


class UserRegisterView(TemplateView):
    template_name = "web/register.html"


class WebLoginView(LoginView):
    template_name = "web/login.html"
    redirect_authenticated_user = True
    redirect_field_name = "next"
    form_class = UserLoginModel

    def form_valid(self, form) -> HttpResponseRedirect:


        return super().form_valid(form)


    def form_invalid(self, form):
        return super().form_invalid(form)
