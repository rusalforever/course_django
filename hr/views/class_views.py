from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from hr.forms import EmployeeForm
from hr.models import Company, Employee

def user_is_superadmin(user) -> bool:
    return user.is_superuser

@method_decorator(cache_page(60 * 3), name='dispatch')
class EmployeeProfileView(DetailView):
    model = Employee
    template_name = 'employee_profile.html'

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.first()
        context['company_logo'] = company.logo.url if company and company.logo else 'static/images/default_logo.png'
        return context

class EmployeeListView(View):
    def get(self, request):
        search = request.GET.get('search', '')
        employees = Employee.objects.all()

        if search:
            employees = employees.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(position__title__icontains=search),
            )

        context = {'employees': employees}
        return render(request, 'employee_list.html', context)

class EmployeeCreateView(UserPassesTestMixin, View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'employee_form.html', {'form': form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('hr:employee_list'))
        return render(request, 'employee_form.html', {'form': form})

    def test_func(self):
        return user_is_superadmin(self.request.user)

class EmployeeUpdateView(UserPassesTestMixin, View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(instance=employee)
        return render(request, 'employee_form.html', {'form': form})

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse('hr:employee_list'))
        return render(request, 'employee_form.html', {'form': form})

    def test_func(self):
        return user_is_superadmin(self.request.user)

class EmployeeDeleteView(UserPassesTestMixin, View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, 'employee_confirm_delete.html', {'object': employee})

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return redirect(reverse('hr:employee_list'))

    def test_func(self):
        return user_is_superadmin(self.request.user)
