from django.urls import path
from examples.querysets import querysets_examples
from . import homework_querysets

urlpatterns = [
    path('querysets/', querysets_examples, name='querysets_examples'),
    path('homework_querysets/', homework_querysets.homework_querysets, name='homework_querysets'),
]
