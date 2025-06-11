import re

from django.forms import BooleanField, CharField, Form
from django.http import HttpRequest

from web.models import User


class UserLoginModel(Form):
    remember_me = BooleanField(required=False)
    username = CharField(max_length=20)

    def __init__(self, *args, request: HttpRequest = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_remember_me(self):
        remember_me = self.data.get('remember_me', None)

        if remember_me == 'on':
            return True

        self.request.session.set_expiry(0)
        return False

    def clean_username(self):
        phone_number = self.data.get('username')
        return re.sub(r'\D', "", phone_number)



    class Meta:
        model = User
        fields = "username", "password", "remember_me"
