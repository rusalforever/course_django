from django.views.generic import DetailView
from hr.models import Employee


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employee'
