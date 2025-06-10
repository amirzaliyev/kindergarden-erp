from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "web/index.html"


class AuthenticateView(TemplateView):
    template_name = "web/authenticate.html"
