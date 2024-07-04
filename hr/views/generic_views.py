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

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class EmployeeListView(SuperUserRequiredMixin, ListView):
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
        employees = context['employees']
        paginator = Paginator(employees, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            employees = paginator.page(page)
        except PageNotAnInteger:
            employees = paginator.page(1)
        except EmptyPage:
            employees = paginator.page(paginator.num_pages)

        context['employees'] = employees
        return context

class EmployeeCreateView(SuperUserRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee_list")

class EmployeeDetailView(SuperUserRequiredMixin, DetailView):
    model = Employee
    template_name = "employee_detail.html"
    context_object_name = "employee"

class EmployeeUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee_list")

class EmployeeDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Employee
    template_name = "employee_confirm_delete.html"
    success_url = reverse_lazy("employee_list")
