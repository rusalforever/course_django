from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from hr.calculate_salary import CalculateMonthRateSalary
from hr.forms import (
    EmployeeForm,
    SalaryForm,
)
from hr.mixins import UserIsAdminMixin
from hr.models import Employee


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(position__title__icontains=search) |
                Q(email__icontains=search),
            )
        return queryset


class EmployeeCreateView(UserIsAdminMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')


class EmployeeUpdateView(UserIsAdminMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')


class EmployeeDeleteView(UserIsAdminMixin, DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')


class EmployeeProfileView(UserIsAdminMixin, DetailView):
    model = Employee
    template_name = 'employee_profile.html'


class SalaryCalculatorView(UserIsAdminMixin, FormView):
    template_name = 'salary_calculator.html'
    form_class = SalaryForm

    def get(self, request, *args, **kwargs):
        form = SalaryForm()
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_employee_id = self.request.POST.get('employee')
        if selected_employee_id:
            context['selected_employee'] = Employee.objects.get(pk=selected_employee_id)
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        employee = cleaned_data.get('employee')

        calculator = CalculateMonthRateSalary(employee=employee)

        days = {day: day_type for day, day_type in cleaned_data.items() if day.startswith(calculator.day_prefix)}

        salary = calculator.calculate_salary(days_dict=days)

        return render(
            self.request,
            self.template_name,
            context={
                'form': form,
                'calculated_salary': salary,
                'selected_employee': employee,
            },
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
