from django.conf.urls import url

from crowdpact.apps.pact.views import PactHomeView

urlpatterns = [
    url(r'', PactHomeView.as_view(), name='pact.index')
]
