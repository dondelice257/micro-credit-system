from rest_framework import viewsets
from rest_framework.response import Response

from apps.authentication.models import User
from apps.authentication.serializers.user import (UserCreationSerializer,
                                                  UserSerializer)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.none()


class UsersListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreationViewSet(viewsets.ViewSet):
    serializer_class = UserCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'response_message': 'user created successfully',
                 'success': True, 'data': serializer.data},
                status=201
                )
        return Response(
            {'response_message': serializer.errors,
             'success': False},
            status=400)
