from rest_framework import serializers

from core.models import User


class EntrepreneurSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class EntrepreneurCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # Enforce user's type
        return User.objects.create_user(type=User.ENTREPRENEUR, **validated_data)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',)


class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'company', )