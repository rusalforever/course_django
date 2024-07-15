from django.shortcuts import render
from .models import Department, Position

def homework_querysets(request):
    # Запит 1
    departments = Department.objects.all()

    # Запит 2:
    positions = Position.objects.all()

    # Запит 3:
    active_positions = Position.objects.filter(is_active=True)

    # Запит 4:
    manager_positions = Position.objects.filter(is_manager=True)

    # Запит 5:
    specific_department_positions = Position.objects.filter(department_id=1)

    context = {
        'departments': departments,
        'positions': positions,
        'active_positions': active_positions,
        'manager_positions': manager_positions,
        'specific_department_positions': specific_department_positions,
    }
    return render(request, 'homework_querysets.html', context)
