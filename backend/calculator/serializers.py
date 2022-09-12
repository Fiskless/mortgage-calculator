from rest_framework import serializers

from .models import BankOffer


class BankOfferSerializer(serializers.ModelSerializer):
    payment = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        model = BankOffer
        fields = '__all__'

    def create(self, validated_data):
        offer = self.validated_data
        if offer['rate_min'] > offer['rate_max']:
            raise serializers.ValidationError({'error': "Минимальная ипотечная ставка должна быть меньше максимальной"})
        if offer['payment_min'] > offer['payment_max']:
            raise serializers.ValidationError({'error': "Минимальный платеж по ипотеке должна быть меньше максимального"})
        if offer['term_min'] > offer['term_max']:
            raise serializers.ValidationError({'error': "Минимальный срок ипотеки должен быть меньше максимального"})
        return BankOffer.objects.create(**validated_data)

