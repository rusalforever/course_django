import os
from django.views.generic import TemplateView
from hr.models import Company


class HomeViev(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.first()
        if company and company.logo and os.path.isfile(company.logo.path):
            context['company_logo'] = company.logo.url
        else:
            context['company_logo'] = None
        return context
