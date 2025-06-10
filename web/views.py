from django.views.generic import TemplateView

# Create your views here.


class IndexView(TemplateView):
    template_name = "web/index.html"


class AuthenticateView(TemplateView):
    template_name = "web/authenticate.html"
