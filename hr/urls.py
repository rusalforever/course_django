from django.urls import path

from hr.views import generic_views as views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/profile/<int:pk>/', views.EmployeeProfileView.as_view(), name='employee_profile'),
    path('salary-calculator/', views.SalaryCalculatorView.as_view(), name='salary_calculator'),
]
