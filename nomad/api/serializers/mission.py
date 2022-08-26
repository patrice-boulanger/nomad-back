from rest_framework import serializers

from core.models import Mission


class MissionListSerializer(serializers.ModelSerializer):
    company = serializers.CharField()

    class Meta:
        model = Mission
        fields = ('id', 'title', 'start', 'end', 'zipcode',
                  'city', 'company', 'driving_license_required', 'year_experience_required')


class MissionDetailSerializer(serializers.ModelSerializer):
    company = serializers.CharField()

    class Meta:
        model = Mission
        fields = "__all__"


class MissionQueryStringSerializer(serializers.Serializer):
    location = serializers.CharField(
        max_length=5, required=False, help_text="filter missions on a zipcode or a department")
    feature = serializers.ListField(child=serializers.IntegerField(help_text="filter missions on feature id"),
                                    required=False)
