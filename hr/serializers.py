from rest_framework import serializers

from hr.models import (
    Employee,
    Position,
)
from hr.validators import validate_positive, holiday_days, vacation_days


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'position')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'title', 'department', 'is_manager', 'is_active', 'job_description', 'monthly_rate')


class SalarySerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    working_days = serializers.IntegerField(max_value=31)
    holiday_days = serializers.IntegerField(validators=[holiday_days])
    sick_days = serializers.IntegerField(default=0, max_value=4)
    vacation_days = serializers.IntegerField(validators=[vacation_days])

    def validate(self, data):
        total_days = sum([
            data.get('working_days', 0),
            data.get('holiday_days', 0),
            data.get('sick_days',   0),
            data.get('vacation_days', 0),
        ])
        if total_days > 31:
            raise serializers.ValidationError('Total days exceed the number of days in a month.')
        return data

    def validate_sick_days(self, value):
        """
        Checks that the number of sick days does not exceed 3.
        """
        if value > 3:
            raise serializers.ValidationError('The number of sick days cannot be more than 3.')
        return value
