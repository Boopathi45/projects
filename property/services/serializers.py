from rest_framework import serializers

from services.models import Services, EditingPreference, ServiceEditingPreference

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class EditingPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditingPreference
        fields = '__all__'

class ServiceEditingPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEditingPreference
        fields = '__all__'

class ServiceUploadSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        error_messages={
            'required':'Service name is required',
            'blank':'Service name should not be blank'
        }
    )
    price = serializers.DecimalField(
        required=True,
        max_digits=20, 
        decimal_places=2,
        error_messages={
            'required':'Price is required',
            'blank':'Price should not be blank'
        }
    )
    file_type = serializers.CharField(
        required=True,
        error_messages={
            'required':'File type is required',
            'blank':'File type should not be blank'
        }
    )
    preferences_lst = serializers.ListField(
        required=True,
        error_messages={
            'required':'Preference list is required',
            'blank':'Preference list should not be blank or null'
        }
    )