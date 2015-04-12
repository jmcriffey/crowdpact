from django.conf.urls import url

from crowdpact.apps.account.views import AccountLoginView

urlpatterns = [
    url(r'^login/?$', AccountLoginView.as_view(), name='account.login')
]
