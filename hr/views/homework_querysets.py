import json
from django.db.models import Q
from django.http import HttpResponse
from django.core.serializers import serialize
from hr.models import Department, Position
from django.db.models import Count

def departments_with_managers(request):
    departments = Department.objects.annotate(manager_count=Count('position', filter=Q(position__is_manager=True))).filter(manager_count__gt=0).order_by('name')
    res = serialize('json', departments)
    return HttpResponse(res, content_type='application/json')

def active_positions(request):
    active_positions = Position.objects.filter(is_active=True)
    res = serialize('json', active_positions)
    return HttpResponse(res, content_type='application/json')

def active_positions_or_hr(request):
    active_or_hr_positions = Position.objects.filter(Q(is_active=True) | Q(department__name="hr")).order_by('title')
    res = serialize('json', active_or_hr_positions)
    return HttpResponse(res, content_type='application/json')

def departments_with_manager(request):
    departments = Department.objects.annotate(manager_count=Count('position', filter=Q(position__is_manager=True))).values('name', 'manager_count').filter(manager_count__gt=0)
    res = json.dumps(list(departments))
    return HttpResponse(res, content_type='application/json')

def all_sorted_departments(request):
    all_departments = Department.objects.filter(position__is_active=True).order_by('name').values("name", "position__is_active")
    res = json.dumps(list(all_departments))
    return HttpResponse(res, content_type='application/json')

def departments_without_managers(request):
    departments = Department.objects.annotate(manager_count=Count('position', filter=Q(position__is_manager=True))).filter(manager_count=0).order_by('name')
    res = serialize('json', departments)
    return HttpResponse(res, content_type='application/json')

def inactive_positions(request):
    inactive_positions = Position.objects.filter(is_active=False)
    res = serialize('json', inactive_positions)
    return HttpResponse(res, content_type='application/json')
