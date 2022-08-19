from django.utils.translation import gettext_lazy as _

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema

from core.models import Mission

from ..permissions import IsNomadEntrepreneur
from ..serializers import MissionListSerializer, MissionDetailSerializer, MissionQueryStringSerializer

class MissionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
    last_page_strings = (_('last page'),)


class MissionListView(generics.ListAPIView):
    serializer_class = MissionListSerializer
    permission_classes = [IsAuthenticated, IsNomadEntrepreneur, ]
    pagination_class = MissionPagination

    def get_queryset(self):
        missions = Mission.objects.all()

        location = self.request.query_params.get('location')
        if location is not None:
            missions = missions.filter(zipcode__startswith=location)

        features = self.request.query_params.getlist('feature')
        if features:
            try:
                features = list(map(int, features[0].split(',')))
                missions = missions.filter(features__in=features).distinct()
            except Exception as e:
                pass

        return missions

    @swagger_auto_schema(operation_description="Returns available missions. The list can be filtered by location and features of the mission.",
                         operation_id="missions_all_list",
                         query_serializer=MissionQueryStringSerializer(),
                         responses={
                             200: MissionListSerializer,
                             401: "credentials are missing or invalid",
                             503: "internal server error",
                         })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MissionDetailView(generics.RetrieveAPIView):
    serializer_class = MissionDetailSerializer
    permission_classes = [IsAuthenticated, IsNomadEntrepreneur, ]
    queryset = Mission.objects.all()
