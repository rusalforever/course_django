from django.shortcuts import render, get_object_or_404
from .models import Employee

def get_employee_email(request):
    try:
        user = Employee.objects.get(email='hliebovsiienko@example.com')
    except Employee.DoesNotExist:
        pass

    return render(request, 'template.html', {'user': user})
