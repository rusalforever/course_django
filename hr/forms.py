from django import forms
from .models import Employee  # Import your Employee model

class EmployeeForm(forms.ModelForm):
    # Assuming 'Employee' is your model name and it has 'name', 'sick_days', and 'holiday_days' fields

    class Meta:
        model = Employee
        fields = ['name', 'sick_days', 'holiday_days', 'salary']  # Add all the fields you need

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
        # Add any additional validation here
        return cleaned_data

    # Read-only field to display the employee's name for whom the salary is calculated
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance and instance.salary:
            self.fields['salary_display'] = forms.CharField(
                label='Salary for',
                initial=f'{instance.name} - {instance.salary}',
                disabled=True,  # This makes the field read-only
            )