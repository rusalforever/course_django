from django.shortcuts import render
from django.db.models import Q
from hr.models import Department, Position


def querysets_homework(request):
    departments_with_manager_positions = Department.objects.filter(position__is_manager=True).distinct().order_by('name')
    total_active_positions = Position.objects.filter(is_active=True).count()
    positions_active_or_hr = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))
    departments_with_managers = Department.objects.filter(position__is_manager=True).values('name').distinct()
    positions_sorted_by_title = Position.objects.order_by('title').values('title', 'is_active')

    context = {
        'departments_with_manager_positions': departments_with_manager_positions,
        'total_active_positions': total_active_positions,
        'positions_active_or_hr': positions_active_or_hr,
        'departments_with_managers': departments_with_managers,
        'positions_sorted_by_title': positions_sorted_by_title,
    }

    return render(request, 'querysets.html', context)
