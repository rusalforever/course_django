from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from hr.forms import EmployeeForm
from hr.models import Employee


def user_is_superadmin(user) -> bool:
    return user.is_superuser


class EmployeeListView(View):
    def get(self, request):
        search = request.GET.get("search", "")
        employees = Employee.objects.all()

        if search:
            employees_test = employees_test.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(position__title__icontains=search)
                | Q(email__icontains=search)
            )

        context = {"employees_test": employees_test}
        return render(request, "employees.html", context)


class EmployeeCreateView(UserPassesTestMixin, View):
    @staticmethod
    def get(request):
        form = EmployeeForm()
        return render(request, 'employee_form.html', {'form': form})

    @staticmethod
    def post(request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("employee_list"))
        return render(request, "employee_form.html", {"form": form})

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeUpdateView(UserPassesTestMixin, View):
    @staticmethod
    def get(request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(instance=employee)
        return render(request, "employee_form.html", {"form": form})

    @staticmethod
    def post(request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse("hr:employees"))
        return render(request, "employee_form.html", {"form": form})

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeDeleteView(UserPassesTestMixin, View):
    @staticmethod
    def get(request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, "employee_confirm_delete.html", {"object": employee})

    @staticmethod
    def post(request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return redirect(reverse("employees"))

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employee'

    @staticmethod
    def get_info(request):
        form = EmployeeForm()
        return render(request, "employee_detail.html", {"form": form})

    @staticmethod
    def post_info(request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("hr:employees"))
        return render(request, "employee_detail.html", {"form": form})

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return redirect(reverse('hr:employee_list'))

    def test_func(self):
        return user_is_superadmin(self.request.user)
