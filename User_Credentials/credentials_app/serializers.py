from rest_framework import serializers

from credentials_app.models import Credentials, User

class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CheckCredentialsSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Title is required',
            'blank': 'Title should not be blank or null'
        }
    )
    description = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Description is required',
            'blank': 'Description should not be null or blank'
        }
    )
    value = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0.0,
        error_messages={
            'required': 'Value is required',
            'max_digit': 'max_digit should not more than 18',
            'blank': 'Value dhould not be blank or null'
        }
    )
    expire_on = serializers.DateTimeField(
        required=True,
        error_messages={
            'required': 'Expiring date is mandatory',
            'blank': 'Expire_on should not be blank or null'
        }
    )
