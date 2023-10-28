from django.db.models import F
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated

from services.serializers import *
from services.utility import get_current_timestamp
from services.models import Services, EditingPreference, ServiceEditingPreference

class ServicesListView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        job_id = request.query_params.get('job_id', 0)
        services_objs = Services.objects.all()
        serializer = ServicesSerializer(services_objs, many=True)
        data={
            "message":"Services fetched successfully",
            "services":serializer.data,
        }
        if job_id:
            data['job_id'] = get_current_timestamp()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        service_serializer = ServiceUploadSerializer(data=data)
        service_serializer.is_valid(raise_exception=True)
        data = service_serializer.data
        for price_obj in data['preferences_lst']:
            if int(price_obj['price']) < 0:
                return Response({
                    "message":"Preference price should not be the negative number"
                }, status=status.HTTP_400_BAD_REQUEST) 
        service_obj = Services.objects.create(name=data['name'], price=data['price'], file_type=data['file_type'])
        for preferences in data['preferences_lst']:
            edit_pre_obj = EditingPreference.objects.update_or_create(name=preferences['name'])
            for object in edit_pre_obj:
                ServiceEditingPreference.objects.create(service_id=service_obj, preference_id=object, price=preferences['price'])  
                break 
        return Response({
            "message":"Services created successfully",
        }, status=status.HTTP_200_OK)
    
class ServicesDetailView(APIView):
    permission_classes = ([IsAuthenticated])

    def get_object(self, id):
        try:
            return Services.objects.get(id=id)
        except Exception as e:
            return Http404
        
    def put(self, request, id):
        service_obj = self.get_object(id)
        data = request.data
        serializer = ServicesSerializer(service_obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message":"Services updated successfully",
            "services":serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, id):
        service_obj = self.get_object(id)
        service_obj.delete()
        return Response({
            "message":"Service deleted successfully"
        }, status=status.HTTP_200_OK)
    
class ServiceEditingPreferenceListView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        ser_edit_pre_obj = ServiceEditingPreference.objects.values('price', service_name=F('service_id__name'), preference_name=F('preference_id__name'))
        return Response({
            "message":'Service editing preferences fetched successfully',
            'service_editing_preference':ser_edit_pre_obj
        }, status=status.HTTP_200_OK)