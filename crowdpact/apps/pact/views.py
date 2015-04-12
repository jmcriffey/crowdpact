from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from crowdpact.views import CrowdPactTemplateView


class PactHomeView(CrowdPactTemplateView):
    react_app = 'PactHomeApp'
    title = 'CrowdPact'

    def get(self, request, *args, **kwargs):
        """
        Redirects the user if they are not logged in.
        """
        if not request.user.is_authenticated():
            redirect('pact.home')

        return super(PactHomeView, self).get(request, *args, **kwargs)

    def get_page_data(self):
        page_data = super(PactHomeView, self).get_page_data()
        page_data['user'] = {
            'email': self.request.user.email,
            'username': self.request.user.username
        }
        page_data['logout_url'] = reverse('account.logout')

        return page_data
