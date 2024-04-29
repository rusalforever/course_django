from django.urls import path

from examples.querysets import querysets_homework

urlpatterns = [
    path('querysets/', querysets_homework, name='querysets_homework'),
]
