import json
import os
from django.conf import settings

from django.db.models import (
    Count,
    Q,
)
from django.http import HttpResponse, JsonResponse
from hr.models import (
    Department,
    Position,
)
from django.core.serializers import serialize


def departments_with_managers(request):
    distinct_departments = Department.objects.filter(position__is_manager=True).order_by('name')
    res = serialize('json', distinct_departments)
    return HttpResponse(res)


def active_positions(request):
    active_positions = Position.objects.filter(is_active=True).count()
    return HttpResponse(active_positions)

def active_positions_or_hr(request):
    active_or_hr = Position.objects.filter(is_active=True) | Position.objects.filter(department__name="hr")
    res = serialize('json', active_or_hr)
    return HttpResponse(res)

def departments_with_manager(request):
    departments_with_manager = Department.objects.filter(position__is_manager=True).values('position__is_manager')
    return HttpResponse(departments_with_manager)

def all_sorted_departments(request):
    all_departments = Department.objects.filter(position__is_active=True).order_by('name').values("name", "position__is_active")

    return HttpResponse(all_departments)