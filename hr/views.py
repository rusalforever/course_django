from django.http import JsonResponse
from .models import Department, Position

def homework_querysets(request):
    # Example query: Get all departments
    departments = list(Department.objects.all().values())

    # Example query: Get all positions
    positions = list(Position.objects.all().values())

    # Convert query results to a list of dictionaries
    return JsonResponse({
        'departments': departments,
        'positions': positions
    })