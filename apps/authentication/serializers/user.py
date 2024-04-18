from rest_framework import serializers

from apps.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'last_name',
            'first_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_admin',
            'is_banned'
            ]


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'is_admin'
            ]

    def create(self, validated_data):
        validated_data.pop('otp', None)
        user = User.objects.create_user(**validated_data)
        return user
