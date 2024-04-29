from django.views.generic import UpdateView
from hr.models import Employee
from django.urls import reverse_lazy


class EmployeeEditView(UpdateView):
    model = Employee
    fields = ['username', 'email', 'position']
    template_name = 'employee_edit.html'
    success_url = reverse_lazy('employee_detail')
