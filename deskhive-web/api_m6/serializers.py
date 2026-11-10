"""M6 — serializers for the persistent M5 ORM catalogue and bookings."""
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import OperationalError
from rest_framework import serializers
from spaces.models import Space
from bookings.intervals import local_interval
from bookings.services import save_booking
from deskhive_core.booking import InvalidBookingError, validate_booking

class SpaceSerializer(serializers.ModelSerializer):
    location_city = serializers.CharField(source='location.city', read_only=True)

    class Meta:
        model = Space
        fields = ('code', 'name', 'kind', 'capacity', 'hourly_rate', 'location_city')
        read_only_fields = fields

class BookingCreateSerializer(serializers.Serializer):
    space = serializers.SlugRelatedField(slug_field='code', queryset=Space.objects.all())
    full_name = serializers.CharField(max_length=100, trim_whitespace=True)
    email = serializers.EmailField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    def validate(self, attrs):
        try:
            validate_booking(*local_interval(attrs['start'], attrs['end']))
        except (InvalidBookingError, ValueError) as exc:
            raise serializers.ValidationError({'interval': str(exc)}) from exc
        attrs['email'] = attrs['email'].lower()
        return attrs

    def create(self, validated_data):
        try:
            return save_booking(**validated_data)
        except DjangoValidationError as exc:
            if hasattr(exc, 'message_dict'):
                raise serializers.ValidationError(exc.message_dict) from exc
            raise serializers.ValidationError({'non_field_errors': exc.messages}) from exc
        except OperationalError as exc:
            raise serializers.ValidationError({'non_field_errors': ['Database busy; try again.']}) from exc

class BookingReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    space = serializers.CharField(source='space.code', read_only=True)
    start = serializers.DateTimeField(read_only=True)
    end = serializers.DateTimeField(read_only=True)
