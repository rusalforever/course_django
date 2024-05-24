from rest_framework import serializers

from hr.models import (
    Employee,
    Position,
    Department,
)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'position', 'department')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'title', 'department', 'is_manager', 'is_active', 'job_description', 'monthly_rate')


class SalarySerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    working_days = serializers.IntegerField()
    holiday_days = serializers.IntegerField()
    sick_days = serializers.IntegerField(default=0)
    vacation_days = serializers.IntegerField(default=0)


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('id', 'name', 'parent_department', 'employee_count')

    def get_employee_count(self, obj):
        return obj.employees.count()
