from pipes import Template
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'core/home.html'

    """ def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi Web Playground'
        return context """

    # Redefiniendo el método get
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Web Playground'})

class SamplePageView(TemplateView):
    template_name = 'core/sample.html'