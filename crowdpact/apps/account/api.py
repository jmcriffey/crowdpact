from rest_framework import generics, mixins, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from crowdpact.apps.account.models import Account
from crowdpact.apps.account.serializers import AccountSerializer


class AccountDetailsView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ConfigureEmailView(generics.GenericAPIView):
    """
    Configure email preferences.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        send_emails = request.DATA.get('send_email_notifications', request.user.send_email_notifications)
        request.user.send_email_notifications = send_emails
        request.user.save(update_fields=['send_email_notifications'])

        return Response(status=status.HTTP_201_CREATED)
