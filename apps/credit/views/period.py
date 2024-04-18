from rest_framework import viewsets

from apps.credit.models.period import Period
from apps.credit.serializers.period import PeriodSerializer


class PeriodViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
