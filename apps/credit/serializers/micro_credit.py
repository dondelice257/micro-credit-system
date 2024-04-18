from rest_framework import serializers

from apps.authentication.models import User
from apps.credit.models.micro_credit import MicroCredit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class MicroCreditListSerializer(serializers.ModelSerializer):

    holder=UserSerializer(read_only=True)

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
    holder=UserSerializer(read_only=True)


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
            'created_by',
            'expiration_date',
            'penalties_amount'
        ]

    def create(self, validated_data):
        return MicroCredit.objects.create(**validated_data)


class MicroCreditPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroCredit
        fields = []



    def pay_credit(self):
        self.instance.pay_credit()

    def approve_credit(self):
        self.instance.approve_credit()

    def reject_credit(self):
        self.instance.reject_credit()

    def cancel_credit(self):
        self.instance.cancel_credit()
