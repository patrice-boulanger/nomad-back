from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        """ Force the user to the current request user """
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            raise ValidationError("field user is required for availability")

        return super().save(user=user)

    class Meta:
        model = Availability
        fields = ('id', 'start', 'end', )

