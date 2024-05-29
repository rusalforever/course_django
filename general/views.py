from django.views.generic import TemplateView
from hr.models import Company
import os


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.first()
        if company and company.company_logo and os.path.isfile(company.company_logo.path):
            context['company_logo'] = company.company_logo.url
        else:
            context['company_logo'] = None
        return context
