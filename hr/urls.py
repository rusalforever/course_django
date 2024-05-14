from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from hr.api_views import DepartmentViewSet
from hr.views import generic_views as views


router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)


urlpatterns = [
    path('employees/', cache_page(60, cache='my_key', key_prefix='employee_list')(views.EmployeeListView.as_view()),
         name='employee_list'),
    path(
        'employees/create/',
        views.EmployeeCreateView.as_view(),
        name='employee_create',
    ),
    path(
        'employees/update/<int:pk>/',
        views.EmployeeUpdateView.as_view(),
        name='employee_update',
    ),
    path(
        'employees/delete/<int:pk>/',
        views.EmployeeDeleteView.as_view(),
        name='employee_delete',
    ),
    path(
        'employees/profile/<int:pk>/',
        views.EmployeeProfileView.as_view(),
        name='employee_profile',
    ),
    path(
        'salary-calculator/',
        views.SalaryCalculatorView.as_view(),
        name='salary_calculator',
    ),

    path(
        '',
        include(router.urls)
    ),

]
