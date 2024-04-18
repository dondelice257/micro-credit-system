from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.credit.models.micro_credit import MicroCredit
from apps.credit.serializers.micro_credit import (MicroCreditCreateSerializer,
                                                  MicroCreditDetailsSerializer,
                                                  MicroCreditListSerializer)


class MicroCreditViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MicroCreditListSerializer

    def get_queryset(self):
        queryset = MicroCredit.objects.all()
        user = self.request.user
        if user.is_authenticated:
            is_admin = getattr(user, 'is_admin', False)
            if not is_admin:
                queryset = queryset.filter(holder=user)
        status = self.request.query_params.get('status')
        print('connected', user)

        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MicroCreditDetailsSerializer
        return MicroCreditListSerializer


class MicroCreditCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MicroCreditCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
