from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import FeatureCategory

from ..serializers import AllFeaturesSerializer


class AllFeaturesListView(generics.ListAPIView):
    """ Dumps all features available grouped by feature category. """

    permission_classes = [IsAuthenticated,]
    serializer_class = AllFeaturesSerializer
    queryset = FeatureCategory.objects.prefetch_related("features")


