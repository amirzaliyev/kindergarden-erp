from django.urls import path

from kindergarden_erp.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name='teacher-dashboard'),
]
