from django.shortcuts import render
from rest_framework import viewsets

from apps.authentication.serializers.user import UserCreationSerializer
from rest_framework.response import Response


# Create your views here.


class UserCreationViewSet(viewsets.ViewSet):
    serializer_class = UserCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response_message': 'user created successfully', 'success': True, 'data': serializer.data}, status=201)
        return Response({'response_message': serializer.errors, 'success': False}, status=400)
