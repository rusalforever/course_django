from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)

from hr.forms import EmployeeForm
from hr.models import Employee
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def user_is_superadmin(user) -> bool:
    return user.is_superuser


class EmployeeListView(ListView):
    model = Employee
    template_name = "employee_list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        if search:
            return Employee.objects.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(position__title__icontains=search) |
                Q(email__icontains=search),
            ).order_by("first_name")
        else:
            return Employee.objects.all().order_by("first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class EmployeeCreateView(UserPassesTestMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee_list")

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeDetailView(UserPassesTestMixin, DetailView):
    model = Employee
    template_name = "employee_detail.html"
    context_object_name = "employee"


class EmployeeUpdateView(UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee_list")

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeDeleteView(UserPassesTestMixin, DeleteView):
    model = Employee
    template_name = "employee_confirm_delete.html"
    success_url = reverse_lazy("employee_list")

    def test_func(self):
        return user_is_superadmin(self.request.user)
