from django.db.models import Prefetch

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema

from core.models import FeatureBase, FeatureCategory, Feature

from ..serializers import AllFeaturesSerializer, AllFeaturesQueryStringSerializer


class AllFeaturesListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = AllFeaturesSerializer
#    queryset = FeatureCategory.objects.prefetch_related("features")

    def get_queryset(self):
        if 'context' not in self.request.GET:
            raise ValidationError("missing parameter 'context' in query string")

        context = self.request.GET.get('context')
        scopes = [ FeatureBase.BOTH, ]
        if context == 'mission':
            scopes.append(FeatureBase.ONLY_MISSION)
        elif context == 'profile':
            scopes.append(FeatureBase.ONLY_PROFILE)
        else:
            raise ValidationError(f"invalid context '{context}'")

        # Apply the scope filter on both category & feature
        features_filter = Feature.objects.filter(scope__in=scopes)
        qs = FeatureCategory.objects.prefetch_related(Prefetch("features", queryset=features_filter)).filter(scope__in=scopes)

        return qs

    @swagger_auto_schema(operation_description="Dumps all features available grouped by feature category.",
                         operation_id="features_all_list",
                         query_serializer=AllFeaturesQueryStringSerializer,
                         responses={
                             200: AllFeaturesSerializer,
                             400: "invalid context parameter",
                             401: "credentials are missing or invalid",
                             503: "internal server error",
                         }
)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)