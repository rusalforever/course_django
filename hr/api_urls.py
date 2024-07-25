from django.urls import (
    include,
    path,
)
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from hr.api_views import (
    DepartmentViewSet,
    EmployeeViewSet,
    PositionViewSet,
    SalaryCalculatorView,
    SalaryViewSet,
)


router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'salaries', SalaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('calculate_salary/', SalaryCalculatorView.as_view(), name='calculate_salary'),
]
