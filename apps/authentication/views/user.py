from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.authentication.models import User
from apps.authentication.serializers.user import UserCreationSerializer, UserSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    #Viewset to retrieve user profile information.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Returns the queryset filtered by the authenticated user.
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.none()


class UsersListViewSet(viewsets.ReadOnlyModelViewSet):
    # Viewset to retrieve a list of users.
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreationViewSet(viewsets.ViewSet):
    """
    Viewset for creating a new user instance.
    """
    serializer_class = UserCreationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new user instance.
        """
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
            status=400
        )


class BanUserView(APIView):
    # APIView to ban a user.
    def post(self, request):
        # Ban a user.
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)

        if not user.is_banned:
            user.is_banned = True
            user.save()
            return Response({'message': 'user banned successfully'})
        else:
            return Response({'message': 'user already banned'})
