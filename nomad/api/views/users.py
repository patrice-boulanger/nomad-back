from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import User

from ..serializers import EntrepreneurSerializer, EntrepreneurCreateSerializer, CompanyUserSerializer


class EntrepeneurListView(generics.ListAPIView):
    """ Returns the list of entrepreneurs that an authenticated user can view. """

    serializer_class = EntrepreneurSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        """ Filter the data according to the type of user """
        request = self.request
        user = request.user
        queryset = User.objects.none()

        if user.is_admin:
            queryset = User.objects.filter(type=User.ENTREPRENEUR)
        elif user.is_company:
            pass # TODO
        elif user.is_entrepreneur:
            queryset = User.objects.get(pk=user.pk)  # myself

        return queryset


class EntrepreneurCreateView(generics.CreateAPIView):
    """ Create a new entrepreneur account. """

    serializer_class = EntrepreneurCreateSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Remove the encrypted password from the response
        response.data.pop('password')
        return response


class CompanyUserListView(generics.ListAPIView):
    """ Returns the list of company users that an authenticated user can view. """

    serializer_class = CompanyUserSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        """ Filter the data according to the type of user """
        request = self.request
        user = request.user
        queryset = User.objects.none()

        if user.is_admin:
            queryset = User.objects.filter(type=User.COMPANY)
        elif user.is_company:
            queryset = User.objects.filter(type=User.COMPANY, company=user.company)
        elif user.is_entrepreneur:
            pass  # empty

        return queryset
