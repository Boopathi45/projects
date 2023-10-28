from rest_framework import serializers

from Settings.models import *

class MasterTurnAroundTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTurnAroundTime
        fields = '__all__'

class WorkSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSample
        fields = '__all__'

class UploadTurnAroundTimeSerializer(serializers.Serializer):
    image_count=serializers.CharField(
        required=True,
        error_messages={
            'required':'Image_count is required',
            'blank':'Image_count should not be blank'
        }
    )
    duration_lst=serializers.JSONField(
        required=True,
        error_messages={
            'required':'Duration list is required',
            'blank':'Duration list should not be blank'
        }
    )

class UpdateTurnAroundTimeSerializer(serializers.Serializer):
    id=serializers.IntegerField(
        required=True,
        error_messages={
            'required':'Id is required',
            'blank':'Id should not be blank'
        }
    )
    image_count=serializers.CharField(
        required=True,
        error_messages={
            'required':'Image_count is required',
            'blank':'Image_count should not be blank'
        }
    )
    turn_around_list=serializers.JSONField(
        required=True,
        error_messages={
            'required':'Duration list is required',
            'blank':'Duration list should not be blank'
        }
    )

class GetTurnAroundTimeSerializer(serializers.ModelSerializer):
    turn_around_time_lst = serializers.SerializerMethodField()

    class Meta:
        model = MasterJobImageCount
        fields = ['id', 'image_count', 'turn_around_time_lst']

    def get_turn_around_time_lst(self, turn_around_time_obj):
        return turn_around_time_obj.job_duration.values('id', 'duration', 'price')
    
class UploadWorkSampleSerializer(serializers.Serializer):
    media_type = serializers.CharField(
        required=True,
        error_messages={
            'required':'Media type is required',
            'blank':'Media type should not be blank or null'
        }
    )
    image = serializers.FileField(
        required=True,
        error_messages={
            'required':'Image is required',
            'blank':'Image should not be empty'
        }
    )