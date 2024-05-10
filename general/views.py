from django.views.generic import TemplateView
from hr.models import Company

class HomeViev(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.first()
        context['company'] = Company
        if Company and Company.logo:
            context['logo_url'] = Company.logo
        else:
            context['logo_url'] = 'logo/'
        return context
