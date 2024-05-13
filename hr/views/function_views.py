from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from hr.forms import EmployeeForm
from hr.models import Employee


def user_is_superadmin(user) -> bool:
    return user.is_superuser


@user_passes_test(user_is_superadmin)
def employees(request):
    search = request.GET.get("search", "")
    employees_test = Employee.objects.all()

    if search:
        employees_test = employees_test.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(position__title__icontains=search)
            | Q(email__icontains=search),
        )

    for employee in employees_test:
        print(employee.birth_date)

    context = {"employees_test": employees_test}
    return render(request, "employees.html", context)


@user_passes_test(user_is_superadmin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("hr:employees"))
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})


@user_passes_test(user_is_superadmin)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    context = {"employee": employee}
    return render(request, "employee_detail.html", context)


@user_passes_test(user_is_superadmin)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse("hr:employees"))
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})


@user_passes_test(user_is_superadmin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect(reverse("hr:employees"))
    return render(request, "employee_confirm_delete.html", {"object": employee})
