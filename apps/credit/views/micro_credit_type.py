from rest_framework import viewsets

from apps.credit.models.micro_credit_type import MicroCreditType
from apps.credit.serializers.micro_credit_type import MicroCreditTypeSerializer


class MicroCreditTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MicroCreditTypeSerializer
    queryset = MicroCreditType.objects.all()
