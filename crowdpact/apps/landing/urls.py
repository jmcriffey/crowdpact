from django.conf.urls import url

from crowdpact.apps.landing.views import LandingView, LandingHomeView

urlpatterns = [
    url(r'', LandingView.as_view(), name='landing.index'),
    url(r'$home/?^', LandingHomeView.as_view(), name='landing.home')
]
