from django.shortcuts import render
from .models import Department, Position

def homework_querysets(request):
    # Query 1: All departments
    departments = Department.objects.all()

    # Query 2: All positions
    positions = Position.objects.all()

    # Query 3: Active positions
    active_positions = Position.objects.filter(is_active=True)

    # Query 4: Manager positions
    manager_positions = Position.objects.filter(is_manager=True)

    # Query 5: Positions in a specific department (e.g., department with id=1)
    specific_department_positions = Position.objects.filter(department_id=1)

    context = {
        'departments': departments,
        'positions': positions,
        'active_positions': active_positions,
        'manager_positions': manager_positions,
        'specific_department_positions': specific_department_positions,
    }
    return render(request, 'homework_querysets.html', context)
