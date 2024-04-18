from rest_framework import serializers
from apps.authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for retrieving user data.
    """
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
    """
    Serializer for creating a new user.
    """
    # Adding a write-only field for password
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
            'is_admin',
            'is_staff',
            'is_superuser'
        ]

    def create(self, validated_data):
        # Creating a new user instance using create_user method
        user = User.objects.create_user(**validated_data)
        return user
