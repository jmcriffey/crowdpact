from django.conf.urls import url

from crowdpact.apps.account.views import AccountLoginView, AccountSignupView

urlpatterns = [
    url(r'^login/?$', AccountLoginView.as_view(), name='account.login'),
    url(r'^signup/?$', AccountSignupView.as_view(), name='account.signup')
]
