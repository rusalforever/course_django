from django.contrib import admin
from .models import Employee, Company, Position

# Custom admin actions
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

make_active.short_description = "Mark selected employees as active"

# EmployeeAdmin class
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'position', 'department', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'email')
    actions = [make_active]

    # Custom form layout
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone_number')
        }),
        ('Job Information', {
            'fields': ('position', 'department', 'is_active')
        }),
    )

# Register other models
admin.site.register(Company)
admin.site.register(Position)
