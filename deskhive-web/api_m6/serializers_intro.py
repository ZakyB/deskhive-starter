"""M6 Lab 1: plain DRF Serializer for an existing DeskHive Space.

No API or database write is needed for this activity.
"""
from decimal import Decimal
from rest_framework import serializers


class SpaceSnapshotSerializer(serializers.Serializer):
    """Serialize a Space and validate a matching incoming dictionary."""

    code = serializers.SlugField(max_length=30)
    name = serializers.CharField(max_length=100)
    kind = serializers.ChoiceField(choices=('desk', 'meeting_room'))
    capacity = serializers.IntegerField(min_value=1)
    hourly_rate = serializers.DecimalField(
        max_digits=7, decimal_places=2, min_value=Decimal('0.01')
    )