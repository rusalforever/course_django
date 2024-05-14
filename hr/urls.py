from django.urls import path

from examples.querysets import querysets_homework
from hr.views import class_views as views
from hr.views.employee_edit_view import EmployeeEditView
from hr.views.employee_info_views import EmployeeDetailView
from hr.views.generic_views import EmployeeListView, SalaryCalculatorView, EmployeeProfileView

urlpatterns = [
    path("employees_test/", views.EmployeeListView.as_view(), name="employees"),
    path(
        "employees_test/create/", views.EmployeeCreateView.as_view(), name="employee_create"
    ),
    path(
        "employees_test/update/<int:pk>/", views.EmployeeUpdateView.as_view(), name="employee_update",
    ),
    path(
        "hr/employees/delete/<int:pk>/", views.EmployeeDeleteView.as_view(), name="employee_delete",
    ),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/<int:pk>/edit/', EmployeeEditView.as_view(), name='employee_edit'),
    path("employees/", EmployeeListView.as_view(), name="employees"),
    path('querysets/', querysets_homework, name='querysets_homework'),
    path('salary_calculator', SalaryCalculatorView.as_view(), name='salary_calculator'),
    path('employees/employee_profile/<int:pk>/', EmployeeProfileView.as_view(), name='employee_profile'),


]
