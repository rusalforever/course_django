import calendar
from datetime import date

from django import forms
from django.forms import ChoiceField

from django.core.exceptions import ValidationError

from common.enums import WorkDayEnum
from hr.models import Employee


WorkDayChoices = [(tag.name, tag.value) for tag in WorkDayEnum]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'email', 'position')


class SalaryForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)

        today = date.today()
        _, num_days = calendar.monthrange(today.year, today.month)

        for day in range(1, num_days + 1):
            weekday_name = calendar.day_name[calendar.weekday(today.year, today.month, day)]
            field_name = f'day_{day}'

            if calendar.weekday(today.year, today.month, day) >= 5:  # Saturday and Sunday
                self.fields[field_name] = ChoiceField(
                    label=f'{day} - {weekday_name}',
                    choices=[(WorkDayEnum.WEEKEND.name, WorkDayEnum.WEEKEND.value)],
                    initial=WorkDayEnum.WEEKEND.name,
                )
            else:
                self.fields[field_name] = ChoiceField(
                    label=f'{day} - {weekday_name}',
                    choices=WorkDayChoices,
                    initial=WorkDayEnum.WORKING_DAY.name,
                )

    def clean_employee(self):
        employee = self.cleaned_data.get('employee')
        if not employee:
            raise ValidationError("Employee field must be filled.")
        return employee

    def clean(self):
        cleaned_data = super().clean()
        sick_days = 0
        holiday_days = 0

        for field_name, value in cleaned_data.items():
            if field_name.startswith('day_'):
                if value == WorkDayEnum.SICK_DAY.name:
                    sick_days += 1
                elif value == WorkDayEnum.HOLIDAY.name:
                    holiday_days += 1

        if sick_days > 5:
            raise ValidationError("The number of sick days cannot exceed 5.")

        if holiday_days > 3:
            raise ValidationError("The number of holiday days cannot exceed 3.")

        return cleaned_data