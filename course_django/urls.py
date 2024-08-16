"""
URL configuration for course_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from general.schema import schema_view
from general.views import HomeViev
from hr.api_views import EmployeeViewSet, PositionViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'positions', PositionViewSet, basename='position')

urlpatterns = [
    path('hr/', include(('hr.urls', 'hr'), namespace='hr')),
    path('api/hr/', include(('hr.api_urls', 'api-hr'), namespace='api-hr')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('employees/', include('hr.urls')),
]

urlpatterns += i18n_patterns(
    path('', HomeViev.as_view(), name='home'),
    path('hr_super_secret_admin/', admin.site.urls),
    path('examples/', include('examples.urls')),
    path(
        'accounts/',
        include(('accounts.urls', 'accounts'), namespace='accounts'),
    ),
    path('i18n/', include('django.conf.urls.i18n')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
