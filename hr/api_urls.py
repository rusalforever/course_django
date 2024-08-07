from django.urls import (
    include,
    path,
)
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from hr.api_views import (
    EmployeeViewSet,
    DepartmentViewSet,
    PositionViewSet,
    SalaryCalculatorView,
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('calculate_salary/', SalaryCalculatorView.as_view(), name='calculate_salary'),
]
