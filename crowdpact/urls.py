from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^account/', include('crowdpact.apps.account.urls')),
    url(r'^admin/', include(admin.site.urls))
]
