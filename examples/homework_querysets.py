from django.shortcuts import render
from django.db.models import Q
from .models import Department, Position

def homework_querysets(request):
    # Запит 1
    departments_with_managers = Department.objects.filter(position__title='Manager').order_by('name')

    # Запит 2   
    total_active_positions = Position.objects.filter(is_active=True).count()

    # Запит 3
    active_or_hr_positions = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))

    # Запит 4
    departments_with_managers_names = Department.objects.filter(position__title='Manager').values('name')

    # Запит 5
    positions_sorted_by_name = Position.objects.order_by('name').values('name', 'is_active')

    context = {
        'departments_with_managers': departments_with_managers,
        'total_active_positions': total_active_positions,
        'active_or_hr_positions': active_or_hr_positions,
        'departments_with_managers_names': departments_with_managers_names,
        'positions_sorted_by_name': positions_sorted_by_name,
    }

    return render(request, 'your_template.html', context)
