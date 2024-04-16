from django.contrib import admin

# Register your models here.
from company.models import Company, Employee, Position
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Position)


