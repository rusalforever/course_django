from django.db.models import Q
from django.http import JsonResponse

from hr.models import Department, Position


def homework_querysets(request):
    departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')
    active_positions_count = Position.objects.filter(is_active=True).count()
    positions_active_or_hr = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))
    departments_with_managers_names = Department.objects.filter(position__is_manager=True).values_list('name', flat=True)
    positions_sorted_by_name = Position.objects.order_by('title').values('title', 'is_active')

    response_data = {
        'departments_with_managers': list(departments_with_managers.values()),
        'active_positions_count': active_positions_count,
        'positions_active_or_hr': list(positions_active_or_hr.values()),
        'departments_with_managers_names': list(departments_with_managers_names),
        'positions_sorted_by_name': list(positions_sorted_by_name),
    }

    return JsonResponse(response_data)

