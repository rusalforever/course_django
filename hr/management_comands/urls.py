from django.urls import path

from hr.management_comands.querysets import queryset


urlpatterns = [
    path('queryset/', queryset, name='queryset'),
]
