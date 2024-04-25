from django.urls import path
from hr.views import class_views as views
from hr.views.employee_edit_view import EmployeeEditView
from hr.views.employee_info_views import EmployeeDetailView
from hr.views.generic_views import EmployeeListView

urlpatterns = [
    path("employees/", views.EmployeeListView.as_view(), name="employee_list"),
    path(
        "employees/create/", views.EmployeeCreateView.as_view(), name="employee_create"
    ),
    path(
        "employees/update/<int:pk>/", views.EmployeeUpdateView.as_view(), name="employee_update",
    ),
    path(
        "employee_list/delete/<int:pk>/", views.EmployeeDeleteView.as_view(), name="employee_delete",
    ),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/<int:pk>/edit/', EmployeeEditView.as_view(), name='employee_edit'),
    path("employee_list/", EmployeeListView.as_view(), name="employee_list")
]

# from hr.views.function_views import (
#     employee_create,
#     employee_delete,
#     employee_list,
#     employee_update,
# )
#
#
# urlpatterns = [
#     path('employees/', employee_list, name='employee_list'),
#     path('employees/create/', employee_create, name='employee_create'),
#     path('employees/update/<int:pk>/', employee_update, name='employee_update'),
#     path('employees/delete/<int:pk>/', employee_delete, name='employee_delete'),
# ]
