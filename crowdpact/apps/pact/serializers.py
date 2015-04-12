from rest_framework import serializers

from crowdpact.apps.pact.models import Pact


class PactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pact
        fields = (
            'creator', 'name', 'description', 'goal', 'deadline', 'creation_time', 'goal_met',
            'pledge_count',
        )
