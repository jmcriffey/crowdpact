from django.core.urlresolvers import reverse

from crowdpact.views import CrowdPactTemplateView


class LandingView(CrowdPactTemplateView):
    title = 'CrowdPact - It\'s where crowds make pacts.'

    def get_page_data(self):
        page_data = super(LandingView, self).get_page_data()
        page_data['login_url'] = reverse('account.login')
        page_data['signup_url'] = reverse('account.signup')
        page_data['landing_text_large'] = 'Welcome to CrowdPact.'
        page_data['landing_text_small'] = 'It\'s where crowds make pacts.'
        page_data['pacts'] = [{
            'title': 'Most Popular',
            'items': self.get_most_popular_pacts()
        }, {
            'title': 'Newest',
            'items': self.get_newest_pacts()
        }, {
            'title': 'Ending Soon',
            'items': self.get_ending_soon()
        }]

        return page_data

    def get_most_popular_pacts(self):
        return []

    def get_newest_pacts(self):
        return []

    def get_ending_soon(self):
        return []
