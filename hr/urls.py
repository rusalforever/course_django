from django.urls import path
from django.views.decorators.cache import cache_page
from .views import generic_views as views
from .views import DepartmentViewSet, PositionViewSet, EmployeeViewSet

urlpatterns = [
    path(
        "employees/",
        cache_page(60, cache="my_key", key_prefix="employee_list")(
            views.EmployeeListView.as_view()
        ),
        name="employee_list",
    ),
    path(
        "employees/create/",
        views.EmployeeCreateView.as_view(),
        name="employee_create",
    ),
    path(
        "employees/update/<int:pk>/",
        views.EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
    path(
        "employees/delete/<int:pk>/",
        views.EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
    path(
        "employees/profile/<int:pk>/",
        views.EmployeeProfileView.as_view(),
        name="employee_profile",
    ),
    path(
        "salary-calculator/",
        views.SalaryCalculatorView.as_view(),
        name="salary_calculator",
    ),
    
    path('departments/', DepartmentViewSet.as_view({'get': 'list'}), name='department-list'),
    path('positions/', PositionViewSet.as_view({'get': 'list'}), name='position-list'),
    path('employee-viewset/', EmployeeViewSet.as_view({'get': 'list'}), name='employee-viewset-list'),
]
