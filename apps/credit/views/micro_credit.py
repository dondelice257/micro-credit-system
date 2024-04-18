from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.models import User
from apps.credit.models.micro_credit import MicroCredit
from apps.credit.serializers.micro_credit import (MicroCreditCreateSerializer,
                                                  MicroCreditDetailsSerializer,
                                                  MicroCreditListSerializer, MicroCreditPaySerializer)

from permissions import IsAdmin

from django.utils import timezone


class MicroCreditViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MicroCreditListSerializer

    def get_queryset(self):
        queryset = MicroCredit.objects.all()

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by date
        date_filter = self.request.query_params.get('date')
        if date_filter == 'approaching_payment':
            # Filter credits with expiration date within the next 7 days
            queryset = queryset.filter(expiration_date__lte=timezone.now() + timezone.timedelta(days=7))
        elif date_filter == 'late':
            # Filter credits with expiration date in the past
            queryset = queryset.filter(expiration_date__lt=timezone.now())

        # Additional filtering based on user authentication and role
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return queryset
            else:
                return queryset.filter(holder=self.request.user)

        return queryset.none()


class MicroCreditCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Endpoint for creating a new micro credit
        serializer = MicroCreditCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayCreditView(APIView):
    def post(self, request):
        try:
            # Endpoint for paying off a micro credit
            credit_id = request.data.get("credit_id")
            credit = MicroCredit.objects.get(pk=credit_id)
            serializer = MicroCreditPaySerializer(instance=credit, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.pay_credit()
            return Response({'message': 'Credit paid successfully'}, status=status.HTTP_200_OK)

        except MicroCredit.DoesNotExist:
            return Response({'message': 'Credit not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActionToCreditView(APIView):
    permission_classes=[IsAdmin]

    def post(self, request):
        try:
            # Endpoint for performing actions on a micro credit (approve, reject, cancel)
            credit_id = request.data.get("credit_id")
            action = request.data.get('action')
            credit = MicroCredit.objects.get(pk=credit_id)
            serializer = MicroCreditPaySerializer(instance=credit, data=request.data)
            serializer.is_valid(raise_exception=True)

            if action == 'approve':
                if credit.status == 'INITIAL':
                    serializer.approve_credit()
                    return Response({'message': 'Credit approved successfully'}, status=status.HTTP_200_OK)
                elif credit.status == 'PENDING':
                    return Response({'message': 'The credit has already been approved'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Cannot approve this credit in its current state'},
                                    status=status.HTTP_400_BAD_REQUEST)

            elif action == 'reject':
                if credit.status == 'INITIAL':
                    serializer.reject_credit()
                    return Response({'message': 'Credit rejected successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Cannot reject this credit in its current state'},
                                    status=status.HTTP_400_BAD_REQUEST)

            elif action == 'cancel':
                if credit.status == 'PENDING':
                    serializer.cancel_credit()
                    return Response({'message': 'Credit cancelled successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Cannot cancel this credit in its current state'},
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        except MicroCredit.DoesNotExist:
            return Response({'message': 'Credit not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
