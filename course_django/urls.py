from django.contrib import admin
from django.urls import (
    include,
    path,
)
from hr.views.generic_views import EmployeeListView
from hr.views import class_views as views


urlpatterns = [
    path("", include("hr.urls")),
    path("hr_super_secret_admin/", admin.site.urls),
    path("employee_info/", admin.site.urls),
    path("employee_list/", EmployeeListView.as_view(), name="employee_list"),
    path("employee_list/", views.EmployeeListView.as_view(), name="employee_list"),
]
