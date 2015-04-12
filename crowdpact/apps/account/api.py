from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from crowdpact.apps.account.models import Account
from crowdpact.apps.account.serializers import AccountSerializer


# ############### Abstract API views ################
class AccountDetailsView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
