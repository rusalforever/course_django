from django.db.models import Count, Q
from django.http import JsonResponse
from hr.models import Department, Position

def querysets_examples(request):
    departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')

    total_active_positions = Position.objects.filter(is_active=True).count()

    active_or_hr_positions = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))

    departments_with_managers_names = Department.objects.filter(position__is_manager=True).values('name')

    positions_titles_and_activity = Position.objects.order_by('title').values('title', 'is_active')

    results = {
        'departments_with_managers': list(departments_with_managers.values('name')),
        'total_active_positions': total_active_positions,
        'active_or_hr_positions': list(active_or_hr_positions.values('title', 'is_active')),
        'departments_with_managers_names': list(departments_with_managers_names),
        'positions_titles_and_activity': list(positions_titles_and_activity),
    }

    return JsonResponse(results)
