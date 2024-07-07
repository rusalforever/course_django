from django.core.validators import MaxValueValidator
from rest_framework import serializers

# Custom validator for holiday_days
def validate_holiday_days(value):
    if value > 10:
        raise serializers.ValidationError("Holiday days cannot exceed 10.")

class SalarySerializer(serializers.Serializer):
    # ... other fields ...

    vacation_days = serializers.IntegerField()
    working_days = serializers.IntegerField(validators=[MaxValueValidator(31)])
    holiday_days = serializers.IntegerField(validators=[validate_holiday_days])

    def validate_vacation_days(self, value):
        if value > 5:
            raise serializers.ValidationError("Vacation days cannot exceed 5.")
        return value