from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import WorkLocation


class WorkLocationBaseSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        """ Force the user to the current request user """
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            raise ValidationError("field user is required for work location")

        return super().save(user=user)


class WorkLocationWriteSerializer(WorkLocationBaseSerializer):

    class Meta:
        model = WorkLocation
        fields = ('zipcode', )


class WorkLocationReadSerializer(WorkLocationBaseSerializer):

    class Meta:
        model = WorkLocation
        fields = ('id', 'zipcode', 'city', 'department', 'department_name', 'region', 'latitude', 'longitude', )
