from __future__ import annotations

import re

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.fields import CharField
from django.forms import BooleanField, ValidationError
from authentication.models import User


class UserAuthForm(AuthenticationForm):
    remember_me = BooleanField(required=False)
    username = CharField(max_length=25)

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_remember_me(self):
        remember_me = self.data.get("remember_me", None)

        if remember_me == "on":
            return True

        return False

    def clean_username(self):
        phone_number = self.data.get("username", "")
        phone_number = re.sub(r"\D", "", phone_number)  # type: ignore
        return phone_number

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if not self.user_cache:
                raise ValidationError("Invalid username or password")

            if not self.user_cache.is_active:
                raise ValidationError("Account is disabled")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    class Meta:
        model = User
        fields = "username", "password", "remember_me"
