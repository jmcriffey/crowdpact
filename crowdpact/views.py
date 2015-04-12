import json

from django.http import HttpResponse
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView, View


class CrowdPactContextMixin(ContextMixin):
    def get_context_data(self):
        context = super(CrowdPactContextMixin, self).get_context_data()

        context['page_data'] = json.dumps(self.get_page_data())
        context['react_app'] = self.react_app
        context['title'] = self.get_title()

        return context

    def get_title(self):
        return self.title

    def get_page_data(self):
        return {}

    def get_json_response(self, response=None, status=200):
        response = response or {}

        return HttpResponse(json.dumps(response), status=status)


class CrowdPactTemplateView(CrowdPactContextMixin, TemplateView):
    react_app = 'LandingApp'
    template_name = 'index.html'
    title = 'Welcome to CrowdPact'


class CrowdPactView(CrowdPactContextMixin, View):
    pass
