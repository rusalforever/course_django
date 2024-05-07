from django.views.generic import TemplateView


class HomeViev(TemplateView):
    template_name = "home.html"
