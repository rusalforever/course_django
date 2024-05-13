import datetime

from django.contrib import messages
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

from common.enums import WorkDayEnum
from hr.calculate_salary import CalculateMonthRateSalary
from hr.forms import (
    EmployeeForm,
    SalaryForm,
)
from hr.mixins import UserIsAdminMixin
from hr.models import Employee


class EmployeeListView(ListView):
    model = Employee
    template_name = "employees.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(position__title__icontains=search)
                | Q(email__icontains=search),
            )
        return queryset


class EmployeeCreateView(UserIsAdminMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('hr:employee_list')


class EmployeeUpdateView(UserIsAdminMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('hr:employee_list')


class EmployeeDeleteView(UserIsAdminMixin, DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('hr:employee_list')


class EmployeeProfileView(UserIsAdminMixin, DetailView):
    model = Employee
    template_name = 'employee_profile.html'


class SalaryCalculatorView(UserIsAdminMixin, FormView):
    template_name = 'salary_calculator.html'
    form_class = SalaryForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        employee = form.cleaned_data.get("employee")
        cleaned_data = form.cleaned_data
        employee = cleaned_data.get('employee')

        calculator = CalculateMonthRateSalary(employee=employee)
        days = {
            day: day_type
            for day, day_type in form.cleaned_data.items()
            if day.startswith(calculator.day_prefix)
        }

        sick_days = sum(1 for day, day_type in days.items() if day_type == WorkDayEnum.SICK_DAY.name)
        if sick_days > 5:
            form.errors["sick_days"] = ["The number of sick days can't be more than 5"]
            return self.form_invalid(form)

        holiday_days = sum(1 for day, day_type in days.items() if day_type == WorkDayEnum.HOLIDAY.name)
        if holiday_days > 3:
            form.errors["holiday_days"] = ["The number of holiday days can't be more than 3"]
            return self.form_invalid(form)

        salary = calculator.calculate_salary(days_dict=days)
        calculator.save_salary(salary=salary, date=datetime.date.today())
        employee_name = f'{employee.first_name}{employee.last_name}'

        return render(
            request=self.request,
            template_name=self.template_name,
            context={
                "form": form,
                "calculated_salary": salary,
                "employee_name": employee_name,
            },
        )

    def form_invalid(self, form):
        return super().form_invalid(form)
