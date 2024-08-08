from rest_framework import viewsets
from hr.models import Department
from hr.serializers import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
