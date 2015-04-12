import json

from django.http import HttpResponse
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView, View


class CrowdPactContextMixin(ContextMixin):
    def get_context_data(self):
        context = super(CrowdPactContextMixin, self).get_context_data()

        context['title'] = self.title
        context['app'] = self.app
        context['page_data'] = json.dumps(self.get_page_data())

        return context

    def get_page_data(self):
        return {}

    def get_json_response(self, response=None, status=200):
        response = response or {}

        return HttpResponse(json.dumps(response), status=status)


class CrowdPactTemplateView(CrowdPactContextMixin, TemplateView):
    app = 'LandingApp'
    template_name = 'index.html'
    title = 'Welcome'


class CrowdPactView(CrowdPactContextMixin, View):
    pass
