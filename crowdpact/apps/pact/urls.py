from django.conf.urls import url

from crowdpact.apps.pact.api import EndingSoonPactList, MostPopularPactList, NewestPactList, PactDetailsView

urlpatterns = [
    url(r'^api/details/(?P<id>.+)/?$', PactDetailsView.as_view(), name='pact.api.details'),
    url(r'^api/most-popular/?$', MostPopularPactList.as_view(), name='pact.api.most_popular'),
    url(r'^api/newest/?$', NewestPactList.as_view(), name='pact.api.newest'),
    url(r'^api/ending-soon/?$', EndingSoonPactList.as_view(), name='pact.api.ending_soon'),
]
