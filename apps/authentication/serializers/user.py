from rest_framework import serializers

from apps.authentication.models import User


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_admin']
    def create(self, validated_data):
        validated_data.pop('otp', None)
        user = User.objects.create_user(**validated_data)
        return user
    
    