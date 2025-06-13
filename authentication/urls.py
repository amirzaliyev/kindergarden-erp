from django.urls import path

from .views import IndexView, UserRegisterView, AuthenticationView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", AuthenticationView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
]
