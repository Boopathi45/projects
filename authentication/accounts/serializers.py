from rest_framework import serializers

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required':'Email is required',
            'blank':'Email should not be blank'
        }
    )

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required':'Email is required',
            'blank':'Email should not be blank'
        }
    )
    one_time_pass = serializers.CharField(
        required=True,
        error_messages={
            'required':'One time password (OTP) is required',
            'blank':'One time password (OTP) should not be blank'
        }
    )

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        min_length=8,
        max_length=256,
        error_messages={
            'required': 'Email address is required',
            'blank': 'Email address should not be blank',
            'invalid': 'Enter valid email address'
        }
    )
    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=20,
        error_messages={
            'required': 'Username is required',
            'blank': 'Username should not be blank',
            'min_length': 'Username must have minimum 5 characters',
            'max_length': 'Username must not exceed more than 20 characters'
        }
    )
    first_name = serializers.CharField(
        required=True,
        min_length=3,
        error_messages={
            'required': 'First name is required',
            'blank': 'First name should not be blank',
            'min_length': 'First name must have minimum 3 characters'
        }
    )
    last_name = serializers.CharField(
        required=True,
        min_length=1,
        error_messages={
            'required': 'Last name is required',
            'blank': 'Last name should not be blank',
            'min_length': 'Last name must have minimum 1 character'
        }
    )
    password = serializers.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            'required': 'Password is required',
            'blank': 'Password should not be blank',
            'min_length': 'Password must have minimum 6 characters',
            'max_length': 'Password must not exceed more than 20 characters'
        }
    )
    is_active = serializers.BooleanField(
        default=True
    )
    mobile_number = serializers.CharField(
        required=False,
        max_length=20,
        error_messages={
            'max_length': 'Mobile number should not exceed more than 20 characters'
        }
    )
    headshot = serializers.JSONField(
        required=False
    )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Username is required',
            'blank': 'Username should not be blank'
        }
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Password is required',
            'blank': 'Password should not be blank'
        }
    )