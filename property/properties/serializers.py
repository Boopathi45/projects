from rest_framework import serializers

from properties.models import Property, Wallet

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ['user']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class RawSerializer(serializers.Serializer):
    image = serializers.FileField(
        required=True,
        error_messages={
            'required':'Image is required',
            'blank':'Image should not be blank or empty'
        }
    )