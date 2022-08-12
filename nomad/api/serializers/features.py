from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import FeatureCategory, Feature, User


class FeatureWriteSerializer(serializers.Serializer):
    features = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        features = validated_data['features']

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            try:
                user.features.set(features)
            except IntegrityError:
                raise ValidationError('at least one feature ID is invalid')

        return {'features': [f.pk for f in user.features.all()] }


class FeatureReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'description', )


class AllFeaturesSerializer(serializers.ModelSerializer):
    features = FeatureReadSerializer(many=True, read_only=True)

    class Meta:
        model = FeatureCategory
        fields = ('name', 'multiple_choices', 'features', )


class AllFeaturesQueryStringSerializer(serializers.Serializer):
    """ Define the context to retrieve the features and categories.

        This field can take the following values and is mandatory:

        <ul>
          <li><b>mission</b>: retrieve features & categories to be displayed on mission description form</li>
          <li><b>profile</b>: retrieve features & categories to be displayed on entrepreneur profile</li>
        </ul>
    """
    context = serializers.CharField(required=True, help_text="""Define the context to display the features. This field is mandatory and can take the values:
<ul>
  <li><b>mission</b>: retrieve features & categories to be displayed on mission description form</li>
  <li><b>profile</b>: retrieve features & categories to be displayed on entrepreneur profile</li>
</ul>
""")
