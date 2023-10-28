from rest_framework import serializers

from Jobs.models import Job, JobPayment

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPayment
        fields = '__all__'

class RawImageUploadSerializer(serializers.Serializer):
    job_id = serializers.CharField(
        required=True,
        error_messages={
            'required':'Job id is required',
            'blank':'Job id should not be blank or null'
        }
    )
    job_image = serializers.FileField(
        required=True,
        error_messages={
            'required':'Job image is required',
            'valid':'Job image should not be empty'
        }
    )

class CreateJobSerializer(serializers.Serializer):
    job_id = serializers.CharField(
        required=True,
        error_messages={
            'required':'Job id is required',
            'blank':'Job id should not be blank or null'
        }
    )
    title = serializers.CharField(
        required=True,
        max_length = 255,
        error_messages={
            'required':'Title is required',
            'blank':'Title should not be blank or null'
        }
    )
    services_lst = serializers.ListField(
        required=True,
        error_messages={
            'required':'Services list is required',
            'blank':'Services list should not be blank or null'
        }
    )
    preferences_lst = serializers.ListField(
        required=True,
        error_messages={
            'required':'Services list is required',
            'blank':'Services list should not be blank or null'
        }
    )
    turn_around_time = serializers.CharField(
        required=True,
        error_messages={
            'required':'Turn around time is required',
            'blank':'Turn around time should not be blank or null'
        }
    )
    media_url = serializers.ListField(
        required=True,
        error_messages={
            'required':'Media url is required',
            'blank':'Media url should not be blank or null'
        }
    )
    summary = serializers.JSONField(
        required=True,
        error_messages={
            'required':'Summary is required',
            'blank':'Summary should not be blank or null'
        }
    )

class JobImageDeleteSerializer(serializers.Serializer):
    job_id=serializers.CharField(
        required=True,
        error_messages={
            'required':'Job id is required',
            'blank':'Job id should not be blank or null'
        }
    )

class ImageDeleteSerializer(serializers.Serializer):
    job_id=serializers.CharField(
        required=True,
        error_messages={
            'required':'Job id is required',
            'blank':'Job id should not be blank or null'
        }
    )
    image_url = serializers.ListField(
        required=True,
        error_messages={
            "required":"Image url is required",
            'blank':"Image url is should not be blank or null"
        }
    )

class JobSummarySerializer(serializers.Serializer):
    image_count = serializers.CharField(
        required=True,
        error_messages={
            'required':'Image count is required',
            'blank':'Image count should not be blank or null'
        }
    )
    services_lst = serializers.ListField(
        required=True,
        error_messages={
            'required':'Service list is required',
            'blank':'Service list should not be blank or null'
        }
    )
    preferences_lst = serializers.ListField(
        required=True,
        error_messages={
            'required':'Preferences list is required',
            'blank':'preferences list should not be blank or null'
        }
    )
    turn_around_time = serializers.CharField(
        required=True,
        error_messages={
            'required':'Turn around time is required',
            'blank':'Turn around time should not be blank or null'
        }
    )

class MultithreadtestSerializer(serializers.Serializer):
    img_file = serializers.FileField(
        required=True,
        error_messages={
            'required':'Job image is required',
            'valid':'Job image should not be empty'
        }
    )