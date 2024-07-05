import calendar
from datetime import date

from django import forms
from django.forms import ChoiceField

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
                    choices=[(WorkDayEnum.WEEKEND.value, WorkDayEnum.WEEKEND.value)],
                    initial=WorkDayEnum.WEEKEND.value,
                )
            else:
                self.fields[field_name] = ChoiceField(
                    label=f'{day} - {weekday_name}',
                    choices=WorkDayChoices,
                    initial=WorkDayEnum.WORKING_DAY.value,
                )

    #SICK_LEAVE
    #SICK_DAY
    def clean(self):
        cleaned_data = super().clean()
        sick_leave_days = 0
        holiday_days = 0

        today = date.today()
        _, num_days = calendar.monthrange(today.year, today.month)

        for day in range(1, num_days + 1):
            field_name = f'day_{day}'
            workday = cleaned_data.get(field_name)

            if workday == WorkDayEnum.SICK_DAY.value:
                sick_leave_days += 1
            elif workday == WorkDayEnum.HOLIDAY.value:
                holiday_days += 1

        if sick_leave_days > 5:
            raise forms.ValidationError("Кількість лікарняних днів не може перевищувати 5.")

        if holiday_days > 3:
            raise forms.ValidationError("Кількість днів відпочинку не може перевищувати 3.")

        return cleaned_data
