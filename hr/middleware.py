from django.utils.deprecation import MiddlewareMixin
from .models import RequestStatistics


class RequestStatisticsMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        stats, created = RequestStatistics.objects.get_or_create(pk=1)
        stats.exception += 1
        stats.save()
