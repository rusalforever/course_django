from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from pydantic import ValidationError

from hr.models import Department, Employee, Position


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_department', 'employee_count')

    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Number of Employees'


@admin.register(Position)
class PositionAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'department', 'is_manager')

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, e)
            super().save_model(request, obj, form, change)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'position', 'hire_date', 'department')
    search_fields = ('username', 'position__title', 'department__name')
