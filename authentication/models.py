from django.apps import apps
from django.contrib.auth.models import AbstractUser, UserManager, make_password
from django.db.models import EmailField
from django.db.models.fields import CharField

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user_object(self, phone_number, email, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        phone_number = GlobalUserModel.normalize_username(phone_number)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given phone_number, email, and password.
        """
        user = self._create_user_object(phone_number, email, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(self, phone_number, email, password, **extra_fields):
        """See _create_user()"""
        user = self._create_user_object(phone_number, email, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    async def acreate_user(
        self, phone_number, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return await self._acreate_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)

    async def acreate_superuser(
        self, phone_number, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = EmailField(unique=True)
    phone_number = CharField(max_length=20, unique=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name  # type: ignore

    class Meta(AbstractUser.Meta):
        db_table = "auth_user"
