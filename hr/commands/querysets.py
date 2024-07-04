from django.db.models import Q
from django.shortcuts import render
from hr.models import Department, Position

def queryset(request):
    task1 = Department.objects.filter(position__is_manager=True).distinct().order_by('name')

    task2 = Position.objects.filter(is_active=True).count()

    task3 = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))

    task4 = Department.objects.filter(position__is_manager=True).values('name').distinct()

    task5 = Position.objects.order_by('title').values('title', 'is_active')

    return render(request, 'query_results.html', {
        'task1': task1,
        'task2': task2,
        'task3': task3,
        'task4': task4,
        'task5': task5,
    })
