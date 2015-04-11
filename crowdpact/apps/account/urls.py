from django.conf.urls import url

from crowdpact.apps.account.views import AccountSignupView

urlpatterns = [
    url(r'^signup/$', AccountSignupView.as_view(), name='account.signup')
]
