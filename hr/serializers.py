from rest_framework import serializers

from hr.models import (
    Employee,
    Position,
    Department,
)


def validate_holiday_days(value):
    if value > 10:
        raise serializers.ValidationError("Кількість святкових днів не може перевищувати 10.")
    return value


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'position')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name', 'title', 'department', 'is_manager', 'is_active', 'job_description', 'monthly_rate')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SalarySerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    working_days = serializers.IntegerField(max_value=31)
    holiday_days = serializers.IntegerField(validators=[validate_holiday_days])
    sick_days = serializers.IntegerField(default=0)
    vacation_days = serializers.IntegerField(default=0)

    def validate_vacation_days(self, value):
        if value > 5:
            raise serializers.ValidationError("Кількість відпускних днів не може перевищувати 5.")
        return value