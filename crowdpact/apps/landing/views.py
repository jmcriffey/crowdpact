from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from crowdpact.apps.pact import models as pact_models
from crowdpact.views import CrowdPactTemplateView


class LandingView(CrowdPactTemplateView):
    app = 'LandingApp'
    title = 'CrowdPact - It\'s where crowds make pacts.'

    def get(self, request, *args, **kwargs):
        """
        Redirects the user if they are already logged in.
        """
        if request.user.is_authenticated():
            redirect('pact.home')

        return super(LandingView, self).get(request, *args, **kwargs)

    def get_page_data(self):
        page_data = super(LandingView, self).get_page_data()
        page_data['login_url'] = reverse('account.login')
        page_data['signup_url'] = reverse('account.signup')
        page_data['landing_text_large'] = 'Welcome to CrowdPact.'
        page_data['landing_text_small'] = 'It\'s where crowds make pacts.'
        page_data['pacts'] = [{
            'title': 'Most Popular',
            'items': pact_models.Pact.objects.get_most_popular()
        }, {
            'title': 'Newest',
            'items': pact_models.Pact.objects.get_newest()
        }, {
            'title': 'Ending Soon',
            'items': pact_models.Pact.objects.get_ending_soon()
        }]

        return page_data
