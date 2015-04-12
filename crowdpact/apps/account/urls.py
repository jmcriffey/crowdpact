from django.conf.urls import url

from crowdpact.apps.account.api import AccountDetailsView, ConfigureEmailView
from crowdpact.apps.account.views import AccountLoginView, AccountLogoutView, AccountSignupView

urlpatterns = [
    url(r'^api/details/(?P<id>.+)/?$', AccountDetailsView.as_view(), name='account.api.details'),
    url(r'^api/configure_email/?$', ConfigureEmailView.as_view(), name='account.api.configure_email'),
    url(r'^login/?$', AccountLoginView.as_view(), name='account.login'),
    url(r'^logout/?$', AccountLogoutView.as_view(), name='account.logout'),
    url(r'^signup/?$', AccountSignupView.as_view(), name='account.signup')
]
