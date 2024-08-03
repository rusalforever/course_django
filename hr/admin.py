from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Employee, Position, Department, Company
import logging

logger = logging.getLogger(__name__)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_department")

class PositionAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "is_manager")

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, e)
            logger.error(f'Error saving model: {e}')
        super().save_model(request, obj, form, change)

class EmployeeAdminForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        position = cleaned_data.get('position')
        if position and position.is_manager:
            existing_manager = Employee.objects.filter(
                position__department=position.department,
                position__is_manager=True
            ).exclude(pk=self.instance.pk if self.instance else None).exists()
            if existing_manager:
                self.add_error('position', f"A manager already exists in the {position.department} department.")
        return cleaned_data

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    form = EmployeeAdminForm
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'department', 'position')
    list_filter = ('position__department', 'position')

    def department(self, obj):
        return obj.position.department if obj.position else None
    department.admin_order_field = 'position__department'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('position__department')

admin.site.register(Position, PositionAdmin)
admin.site.register(Company)
