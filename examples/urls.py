from django.urls import path
from hr.views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    homework_querysets
)

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('querysets/', homework_querysets, name='querysets_examples')
]
