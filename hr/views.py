from django.shortcuts import render
from .models import Department, Position

def homework_querysets(request):
    # Query 1
    departments_with_managers = Department.objects.filter(position__title='Manager').order_by('name')

    # Query 2
    active_positions_count = Position.objects.filter(is_active=True).count()

    # Query 3
    active_positions_or_hr = Position.objects.filter(is_active=True) | Position.objects.filter(department__name='HR')

    # Query 4
    departments_with_managers_names = Department.objects.filter(position__title='Manager').values('name')

    # Query 5
    positions_name_activity = Position.objects.order_by('name').values('name', 'is_active')

    context = {
        'departments_with_managers': departments_with_managers,
        'active_positions_count': active_positions_count,
        'active_positions_or_hr': active_positions_or_hr,
        'departments_with_managers_names': departments_with_managers_names,
        'positions_name_activity': positions_name_activity,
    }

    return render(request, 'your_template.html', context)