from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny

from knox.views import LoginView

from core.models import User


class NomadKnowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', )


# Extends knox LoginView to add documentation
class NomadKnoxLoginView(LoginView):
    authentication_classes = [BasicAuthentication, ]

    def post(self, request, format=None):
        """ Login view to retrieve a token for all subsequent calls requiring authentication.

            This endpoint must be called with basic authentication parameters (username & password) and it will
            return a token if the authentication is successful:

            <pre>
                {
                    "expiry": "2022-08-10T07:34:45.449118+02:00",
                    "token": "a12500f601a3ce9b1afa64a4147fb8e68ec7f7b8d5cba3bec05ed1be61bbe830"
                }
            </pre>

            Finally, all other calls to endpoints requiring authentication will be done with an HTTP header
            <i>Authorization</i> set with the value of the token:

            <pre>
                Authorization: Token a12500f601a3ce9b1afa64a4147fb8e68ec7f7b8d5cba3bec05ed1be61bbe830
            </pre>

        """
        return super().post(request=request, format=format)



