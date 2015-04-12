from django.conf.urls import url

from crowdpact.apps.landing.views import LandingView

urlpatterns = [
    url(r'', LandingView.as_view(), name='landing.index')
]
