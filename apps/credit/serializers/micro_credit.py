from rest_framework import serializers

from apps.credit.models.micro_credit import MicroCredit


class MicroCreditListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MicroCredit
        fields = [
            'id',
            'amount',
            'created_at',
            'holder',
            'status',
            'interest_rate',
            'penalties_rate'
        ]


class MicroCreditDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MicroCredit
        fields = '__all__'


class MicroCreditCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroCredit
        fields = [
            'amount',
            'holder',
            'interest_rate',
            'penalties_rate',
            'created_by'
        ]

    def create(self, validated_data):
        return MicroCredit.objects.create(**validated_data)
