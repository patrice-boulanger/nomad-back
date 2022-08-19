from rest_framework import serializers

from core.models import Mission


class MissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ('title', 'start', 'end', 'zipcode', 'city',)


class MissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = "__all__"


class MissionQueryStringSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=5, required=False, help_text="filter missions on a zipcode or a department")
    feature = serializers.ListField(child=serializers.IntegerField(help_text="filter missions on feature id"),
                                    required=False)
