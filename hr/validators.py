from rest_framework import serializers


def validate_positive(value):
    if value < 0:
        raise serializers.ValidationError('This field must be positive.')

def vacation_days(value):
    if value > 5:
        raise serializers.ValidationError('The number of vacation days should not exceed 5.')

def holiday_days(value):
    if value > 10:
        raise serializers.ValidationError('The number of holidays should not exceed 10.')
