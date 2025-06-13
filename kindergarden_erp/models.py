from django.db.models import (CASCADE, CharField, DateField, ForeignKey,
                              ManyToManyField, Model, TextChoices)
from django.utils import timezone


# Create your models here.
class Child(Model):
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
    birth_date = DateField()
    parents = ManyToManyField(
        "authentication.User", through="kindergarden_erp.ChildParent"
    )

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name  # type: ignore

    @property
    def avatar(self):
        return (self.first_name[0] + self.last_name[0]).upper()  # type: ignore

    @property
    def age(self):
        return timezone.datetime.today().year - self.birth_date.year  # type: ignore

    def __str__(self):
        return f"<Child: {self.full_name}>"

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = "kindergarden_erp_children"


class ChildParent(Model):
    parent = ForeignKey("authentication.User", on_delete=CASCADE)
    child = ForeignKey("kindergarden_erp.Child", on_delete=CASCADE)
    relationship = CharField(
        max_length=255,
        help_text="Description for relationship between child and parent",
    )

    def __str__(self):
        return f"<ChildParent: {self.relationship}>"

    def __repr__(self):
        return self.__str__()


class Attendance(Model):
    class AttendanceTypes(TextChoices):
        PRESENT = "present"
        LATE = "late"
        ABSENT = "absent"

    child = ForeignKey(
        "kindergarden_erp.Child", on_delete=CASCADE, related_name="attendance"
    )
    date = DateField(auto_now_add=True)
    status = CharField(
        max_length=15, choices=AttendanceTypes, default=AttendanceTypes.PRESENT
    )

    def __str__(self):
        return f"<Attendance: {self.date}>"

    def __repr__(self):
        return self.__str__()
