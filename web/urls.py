from django.urls import path

from .views import AuthenticateView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("auth/", AuthenticateView.as_view(), name="auth"),
]
