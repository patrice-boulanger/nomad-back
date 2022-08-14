from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.models import User, Availability, WorkLocation

from ..serializers import (EntrepreneurSerializer, EntrepreneurCreateSerializer,
                           FeatureReadSerializer, FeatureWriteSerializer,
                           AvailabilitySerializer,
                           WorkLocationReadSerializer, WorkLocationWriteSerializer,)

from ..permissions import IsNomadEntrepreneur


me_response = openapi.Response("Current user's information", schema=EntrepreneurSerializer)

class MeView(APIView):
    """ Global view to manage calling user's information """

    permission_classes = [IsAuthenticated, ]
    serializer_class = EntrepreneurSerializer

    def get_queryset(self):
        """ Restrict the queryset to the connected user """
        request = self.request
        user = request.user
        return User.objects.filter(pk=user.pk)

    @swagger_auto_schema(operation_description="Returns all information about the current connected user",
                         operation_id="me_list",
                         responses={
                             200: me_response,
                             401: "credentials are missing or invalid",
                             503: "server internal error",
                         })
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = EntrepreneurSerializer(instance=user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Change information of the current connected user",
                         operation_id="me_update",
                         request_body=EntrepreneurSerializer,
                         responses={
                             200: me_response,
                             400: "one or more fields are invalid",
                             401: "credentials are missing or invalid",
                             503: "server internal error",
                         })
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = EntrepreneurSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MeFeaturesListView(generics.ListAPIView, generics.CreateAPIView):
    """ Retrieve and set features for the current user. """

    permission_classes = [IsAuthenticated, IsNomadEntrepreneur, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FeatureReadSerializer
        elif self.request.method == 'POST':
            return FeatureWriteSerializer
        return None

    def get_queryset(self):
        user = self.request.user
        features = user.features.all()
        return features

    @swagger_auto_schema(operation_description="Retrieve all features for the current user",
                         operation_id="me_features_list",
                         responses={
                             200: FeatureReadSerializer(many=True),
                             401: "credentials are missing or invalid",
                             503: "internal server error"
                         })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Set the features for the current user",
                         operation_id="me_features_create",
                         request_body=FeatureWriteSerializer(),
                         responses={
                             200: FeatureWriteSerializer(),
                             400: "invalid data, unknown feature ID",
                             401: "credentials are missing or invalid",
                             503: "internal server error"
                         })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MeAvailabilityBaseView(generics.GenericAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated, IsNomadEntrepreneur, ]

    def get_queryset(self):
        user = self.request.user
        return Availability.objects.filter(user=user)


class MeAvailabilityListView(MeAvailabilityBaseView, generics.ListAPIView, generics.CreateAPIView):
    pass


class MeAvailabilityDetailView(MeAvailabilityBaseView, generics.UpdateAPIView, generics.DestroyAPIView):
    allowed_methods = ['PATCH', 'DELETE', ]  # remove PUT


class MeWorkLocationBaseView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsNomadEntrepreneur, ]

    def get_queryset(self):
        user = self.request.user
        return WorkLocation.objects.filter(user=user)


class MeWorkLocationListView(MeWorkLocationBaseView, generics.ListAPIView, generics.CreateAPIView):

    def get_serializer_class(self):
        return WorkLocationReadSerializer if self.request.method == 'GET' else WorkLocationWriteSerializer

    def create(self, request, *args, **kwargs):
        """ Returns the auto-completed fields """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(WorkLocationReadSerializer(instance=obj).data, status=status.HTTP_201_CREATED, headers=headers)


class MeWorkLocationDetailView(MeWorkLocationBaseView, generics.UpdateAPIView, generics.DestroyAPIView):
    allowed_methods = ['PATCH', 'DELETE', ]  # remove PUT
    serializer_class = WorkLocationWriteSerializer

    def update(self, request, *args, **kwargs):
        """ Returns the auto-completed fields """
        super().update(request, *args, **kwargs)
        return Response(WorkLocationReadSerializer(self.get_object()).data)

