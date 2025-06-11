from django.urls import path

from .views import IndexView, UserRegisterView, WebLoginView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("auth/login/", WebLoginView.as_view(), name="login"),
    path("auth/register/", UserRegisterView.as_view(), name="register"),
]
