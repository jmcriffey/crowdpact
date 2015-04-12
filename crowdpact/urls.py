from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('crowdpact.apps.landing.urls')),
    url(r'^pact/', include('crowdpact.apps.pact.urls')),
    url(r'^account/', include('crowdpact.apps.account.urls')),
    url(r'^pact/', include('crowdpact.apps.pact.urls')),
    url(r'^admin/', include(admin.site.urls))
]
