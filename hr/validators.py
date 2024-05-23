from rest_framework import serializers


def validate_positive(value):
    if value < 0:
        raise serializers.ValidationError('This field must be positive.')


def validate_holiday_days(value):
    if value > 10:
        raise serializers.ValidationError("Кількість святкових днів не може перевищувати 10!")
    return value
