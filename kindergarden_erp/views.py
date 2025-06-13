from django.views.generic import ListView

from .models import Child


# Create your views here.
class IndexView(ListView):
    template_name = "kindergarden_erp/index.html"
    model = Child
    context_object_name = "children"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        children = context.get("children", [])

        students = []
        for child in children:
            required_fields = {
                "id": child.pk,
                "name": child.full_name,
                "status": child.attendance.create().status.value,
                "age": child.age,
                "avatar": child.avatar,
            }
            students.append(required_fields)
        context.update(students=students)

        return context
