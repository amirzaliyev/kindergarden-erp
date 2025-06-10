from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField

# Create your models here.


class User(AbstractUser):
    username = CharField("phone number", max_length=150)

    class Meta(AbstractUser.Meta):
        db_table = "auth_user"
