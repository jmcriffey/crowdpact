from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from crowdpact.apps.pact.models import Pact
from crowdpact.apps.pact.serializers import PactSerializer


# ############### Abstract API views ################
class BasePactView(generics.GenericAPIView):
    serializer_class = PactSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)


class BasePactList(mixins.ListModelMixin, BasePactView):
    serializer_class = PactSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# ############### Concrete API views ################
class PactDetailsView(mixins.RetrieveModelMixin, BasePactView):
    lookup_field = 'id'
    queryset = Pact.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MostPopularPactList(BasePactList):
    queryset = Pact.objects.live_pacts.most_popular

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NewestPactList(BasePactList):
    queryset = Pact.objects.live_pacts.newest

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EndingSoonPactList(BasePactList):
    queryset = Pact.objects.live_pacts.ending_soon

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
