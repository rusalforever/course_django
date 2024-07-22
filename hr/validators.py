from rest_framework import serializers


def validate_positive(value):
    if value < 0:
        raise serializers.ValidationError('This field must be positive.')


def validate_holiday_days(value):
    if value > 10:
        raise serializers.ValidationError('The "holiday_days" field must be less than or equal to 10.')