from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from hr.calculate_salary import CalculateMonthRateSalary
from hr.models import Employee, Position, Department
from hr.pydantic_models import WorkingDays
from hr.serializers import EmployeeSerializer, DepartmentSerializer, PositionSerializer, SalarySerializer

def get_employee_count(position: Position = None, department: Department = None) -> int:
    if position:
        return Employee.objects.filter(position=position).count()
    elif department:
        positions = Position.objects.filter(department=department)
        return Employee.objects.filter(position__in=positions).count()
    return 0

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @method_decorator(cache_page(60*2))
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(position__title__icontains=search) |
                Q(email__icontains=search),
            )
        return queryset

    @action(detail=True, methods=['get'])
    def position_count(self, request, pk=None):
        employee = self.get_object()
        count = get_employee_count(position=employee.position)
        return Response({'position_count': count})

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=True, methods=['get'])
    def employee_count(self, request, pk=None):
        department = self.get_object()
        count = get_employee_count(department=department)
        return Response({'employee_count': count})

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class SalaryCalculatorView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SalarySerializer(data=request.data)
        if serializer.is_valid():
            try:
                calculator = CalculateMonthRateSalary(employee=serializer.validated_data['employee'])
                month_days = WorkingDays(
                    working=serializer.validated_data['working_days'],
                    sick=serializer.validated_data['sick_days'],
                    holiday=serializer.validated_data['holiday_days'],
                    vacation=serializer.validated_data['vacation_days'],
                )
                salary = calculator.calculate_salary(month_days=month_days)
                return Response({'salary': salary})
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        return Response(serializer.errors, status=400)
