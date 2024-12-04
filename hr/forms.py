from django import forms
from .models import Employee

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee', 'sick_days', 'holiday_days']

    def clean_employee(self):
        employee = self.cleaned_data.get('employee')
        if not employee:
            raise forms.ValidationError("Employee field must be filled.")
        return employee

    def clean(self):
        cleaned_data = super().clean()
        sick_days = cleaned_data.get('sick_days')
        holiday_days = cleaned_data.get('holiday_days')

        if sick_days is not None and sick_days > 5:
            raise forms.ValidationError("The number of sick days cannot exceed 5.")

        if holiday_days is not None and holiday_days > 3:
            raise forms.ValidationError("The number of holiday days cannot exceed 3.")

        return cleaned_data

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'sick_days', 'holiday_days', 'salary']

    def clean_sick_days(self):
        sick_days = self.cleaned_data.get('sick_days')
        if sick_days > 5:
            raise forms.ValidationError("Sick days cannot exceed 5.")
        return sick_days

    def clean_holiday_days(self):
        holiday_days = self.cleaned_data.get('holiday_days')
        if holiday_days > 3:
            raise forms.ValidationError("Holiday days cannot exceed 3.")
        return holiday_days

    def clean(self):
        cleaned_data = super().clean()
        # Додавання будь-яке додаткове підтвердження тут
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance and instance.salary:
            self.fields['salary_display'] = forms.CharField(
                label='Salary for',
                initial=f'{instance.name} - {instance.salary}',
                disabled=True,
            )
