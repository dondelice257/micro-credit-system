from rest_framework import serializers

from apps.credit.models.micro_credit_type import MicroCreditType


class MicroCreditTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroCreditType
        fields='__all__'