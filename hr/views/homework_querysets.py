from django.http import JsonResponse
from models import Department, Position

def homework_querysets(request):
    # Query 1: Departments with manager positions, sorted alphabetically
    departments_with_managers = Department.objects.filter(
        position__title='Manager'
    ).order_by('name').distinct()

    # Query 2: Count of active positions
    active_positions_count = Position.objects.filter(
        is_active=True
    ).count()

    # Query 3: Active positions or positions in the "HR" department
    active_or_hr_positions = Position.objects.filter(
        is_active=True
    ) | Position.objects.filter(
        department__name='HR'
    )

    # Query 4: Names of departments with managers
    departments_with_managers_names = Department.objects.filter(
        position__title='Manager'
    ).values('name').distinct()

    # Query 5: Items sorted by name, displaying only name and activity
    sorted_items = Position.objects.order_by('name').values('name', 'is_active')

    # Convert querysets to lists of dictionaries for JSON response
    return JsonResponse({
        'departments_with_managers': list(departments_with_managers.values()),
        'active_positions_count': active_positions_count,
        'active_or_hr_positions': list(active_or_hr_positions.values()),
        'departments_with_managers_names': list(departments_with_managers_names),
        'sorted_items': list(sorted_items),
    })