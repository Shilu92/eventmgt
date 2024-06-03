from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    pay_id = serializers.CharField(max_length = 200)
    order_id = serializers.CharField(max_length = 200)
    status = serializers.CharField(max_length =20,default = 'success' )
    amount = serializers.DecimalField(max_digits=10,decimal_places=2)
