from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Employee

# Assuming you have an EmployeeListView class that displays a list of employees
class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) |
                Q(position__name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

# This is the EmployeeProfileView class for displaying individual employee details
class EmployeeProfileView(DetailView):
    model = Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employee'
