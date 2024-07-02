from django.http import JsonResponse
from .models import Department, Position

def homework_querysets(request):
    # Query 1: Departments with manager positions, sorted by name
    departments_with_managers = Department.objects.filter(
        positions__title='Manager'
    ).order_by('name').distinct()

    # Query 2: Total number of active positions
    active_positions_count = Position.objects.filter(
        is_active=True
    ).count()

    # Query 3: Active positions or positions in the HR department
    active_or_hr_positions = Position.objects.filter(
        Q(is_active=True) | Q(department__name='HR')
    ).values('title', 'department__name')

    # Query 4: Names of departments with managers
    departments_with_managers_names = Department.objects.filter(
        positions__title='Manager'
    ).values('name').distinct()

    # Query 5: All items sorted by name, displaying only name and activity
    items_sorted_by_name = SomeModel.objects.order_by('name').values('name', 'is_active')

    # Combine the query results into a response dictionary
    response_data = {
        'departments_with_managers': list(departments_with_managers),
        'active_positions_count': active_positions_count,
        'active_or_hr_positions': list(active_or_hr_positions),
        'departments_with_managers_names': list(departments_with_managers_names),
        'items_sorted_by_name': list(items_sorted_by_name),
    }

    # Return the results as JSON
    return JsonResponse(response_data)

# Add the following path to your urls.py:
# path('homework-querysets/', views.homework_querysets, name='homework-querysets')