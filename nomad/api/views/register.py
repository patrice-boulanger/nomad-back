from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..serializers import EntrepreneurCreateSerializer


class EntrepreneurSignUpView(generics.CreateAPIView):
    """ Create a new entrepreneur account. """

    serializer_class = EntrepreneurCreateSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Remove the encrypted password from the response
        response.data.pop('password')
        return response