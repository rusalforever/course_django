from django.shortcuts import render
from django.http import JsonResponse
from hr.models import Department, Position
from django.db.models import Q

def homework_querysets(request):
    departments_with_managers = Department.objects.filter(position__title="Manager").order_by('name')

    active_positions_count = Position.objects.filter(is_active=True).count()

    hr_department_positions = Position.objects.filter(is_active=True).filter(Q(department__name="HR"))

    departments_names_with_managers = Department.objects.filter(position__title="Manager").values('name')

    sorted_positions = Position.objects.all().order_by('title').values('title', 'is_active')

    response_data = {
        'departments_with_managers': list(departments_with_managers.values('name')),
        'active_positions_count': active_positions_count,
        'hr_department_positions': list(hr_department_positions.values('title', 'is_active')),
        'departments_names_with_managers': list(departments_names_with_managers),
        'sorted_positions': list(sorted_positions)
    }

    return JsonResponse(response_data)
