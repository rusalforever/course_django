from django.urls import path
from hr.views import class_views as views
from hr.views import homework_querysets
from django.http import HttpResponse 

urlpatterns = [
    path("", views.home_view, name="home"),
    path("employees/", views.EmployeeListView.as_view(), name="employee_list"),
    path("employees/create/", views.EmployeeCreateView.as_view(), name="employee_create"),
    path("employees/update/<int:pk>/", views.EmployeeUpdateView.as_view(), name="employee_update"),
    path("employees/delete/<int:pk>/", views.EmployeeDeleteView.as_view(), name="employee_delete"),
    path("employees/departments_with_managers/", homework_querysets.departments_with_managers, name="departments_with_managers"),
    path("employees/active_positions/", homework_querysets.active_positions, name="active_positions"),
    path("employees/active_positions_or_hr/", homework_querysets.active_positions_or_hr, name="active_positions_or_hr"),
    path("employees/departments_with_manager/", homework_querysets.departments_with_manager, name="departments_with_manager"),
    path("employees/all_sorted_departments/", homework_querysets.all_sorted_departments, name="all_sorted_departments"),
    path("employees/departments_without_managers/", homework_querysets.departments_without_managers, name="departments_without_managers"),
    path("employees/inactive_positions/", homework_querysets.inactive_positions, name="inactive_positions"),
]

# from hr.views.function_views import (
#     employee_create,
#     employee_delete,
#     employee_list,
#     employee_update,
# )
#
# urlpatterns = [
#     path("employees/", employee_list, name="employee_list"),
#     path("employees/create/", employee_create, name="employee_create"),
#     path("employees/update/<int:pk>/", employee_update, name="employee_update"),
#     path("employees/delete/<int:pk>/", employee_delete, name="employee_delete"),
# ]
