from rest_framework import serializers

from crowdpact.apps.account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'username', 'email', 'human_name', 'about', 'location', 'website', 'photo', 'date_joined',
            'send_email_notifications', 'created_pacts', 'pledges',
        )

    created_pacts = serializers.SerializerMethodField()
    pledges = serializers.SerializerMethodField()

    def get_created_pacts(self, obj):
        from crowdpact.apps.pact.models import Pact
        from crowdpact.apps.pact.serializers import PactSerializer

        return [
            PactSerializer(pact).data for pact in Pact.objects.live_pacts.created_by_user(obj)
        ]

    def get_pledges(self, obj):
        from crowdpact.apps.pact.models import Pact
        from crowdpact.apps.pact.serializers import PactSerializer

        return [
            PactSerializer(pact).data for pact in Pact.objects.live_pacts.pledged_by_user(obj)
        ]
