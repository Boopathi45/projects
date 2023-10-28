from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from Settings.models import *
from Settings.serializers import *
from Settings.utility import upload_work_sample
    
class TurnAroundTime(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        turn_around_time_obj = MasterTurnAroundTime.objects.all()
        serializer = MasterTurnAroundTimeSerializer(turn_around_time_obj, many=True)
        return Response({
            "message":"Turn around time fetched successfully",
            "turn_around_time":serializer.data
        }, status=status.HTTP_200_OK) 

    def post(self, request):
        data = request.data
        serializer = UploadTurnAroundTimeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        image_count = serializer.data['image_count']
        duration_lst = serializer.data['duration_lst']
        unique_lst, turn_aroun_time_lst = [], []
        for dict_obj in duration_lst:
            if dict_obj['duration'] not in unique_lst:
                unique_lst.append(dict_obj['duration'])
            else:
                return Response({
                    "message":"Duration must be unique"
                }, status=status.HTTP_400_BAD_REQUEST)
        if len(unique_lst) == 3:
            image_cnt_obj = MasterJobImageCount.objects.create(image_count=image_count)
            for dict_obj in duration_lst:
                turn_aroun_time_lst.append(
                    MasterTurnAroundTime(
                        duration=dict_obj['duration'],
                        price=dict_obj['price'],
                        image_count_id=image_cnt_obj
                    )
                )
            MasterTurnAroundTime.objects.bulk_create(turn_aroun_time_lst)
            return Response({
                "message":"Turn around time created successfully"
            }, status=status.HTTP_200_OK)    
        else:
            return Response({
                "message":"Duration list count must be 3"
            }, status=status.HTTP_400_BAD_REQUEST)

class TurnAroundTimeDetails(APIView):
    permission_classes = [(IsAuthenticated)]

    def put(self, request):
        data = request.data
        serializer = UpdateTurnAroundTimeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        image_count = serializer.data['image_count']
        img_count_id = serializer.data['id']
        turn_around_list = serializer.data['turn_around_list']
        img_cnt_obj = MasterJobImageCount.objects.filter(id=img_count_id).first()
        img_cnt_obj.image_count=image_count
        img_cnt_obj.save()
        unique_list=[]
        turn_around_list_update_lst=[]
        for dict_obj in turn_around_list:
            if not dict_obj['duration'] in unique_list:
                unique_list.append(dict_obj['duration'])
            else:
                return Response({
                    "message":"Duration must be unique"
                }, status=status.HTTP_400_BAD_REQUEST)
        turn_around_time_id = list( ele['id'] for ele in turn_around_list)
        turn_around_time_obj = MasterTurnAroundTime.objects.filter(id__in=turn_around_time_id, image_count_id=img_cnt_obj.id)
        for index, turn_around in enumerate(turn_around_time_obj):
            turn_around.duration = turn_around_list[index]['duration']
            turn_around.price = turn_around_list[index]['price']
            turn_around_list_update_lst.append(turn_around)
        MasterTurnAroundTime.objects.bulk_update(turn_around_list_update_lst, ['duration', 'price'])
        return Response({
            "message":"Turn around time updated successfully"
        }, status=status.HTTP_200_OK)

class GetTurnAroundTimeView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        image_count = request.query_params.get('image_count')
        if image_count:
            image_count_obj = MasterJobImageCount.objects.prefetch_related('job_duration').filter(image_count__gte=image_count).order_by('image_count').first()
            if image_count_obj:
                serializer = GetTurnAroundTimeSerializer(image_count_obj)
            if not image_count_obj:
                image_count_obj = MasterJobImageCount.objects.prefetch_related('job_duration').filter(image_count__lte=image_count).order_by('image_count').last()
                serializer = GetTurnAroundTimeSerializer(image_count_obj)
            return Response({
                "message":"Turn around time fetched successfully",
                "turn_around_time":serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message":"Image count is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
class WorkSampleListView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        sample_obj = WorkSample.objects.all()
        serializer = WorkSampleSerializer(sample_obj)
        return Response({
            'message':'Work samples fetched successfully',
            'work_sample':serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        user_obj = User.objects.get(id=request.user.id)
        serializer = UploadWorkSampleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        upload_wrk_samp_resp = upload_work_sample(request, data['image'], user_obj.id)
        if upload_wrk_samp_resp['status'] == True:
            image_limit = WorkSample.objects.filter(user_id=user_obj.id).count()
            if not image_limit >= 10 :
                upload_img_url = {"url":upload_wrk_samp_resp['url'], "type":data['media_type']}
                work_sample_obj = WorkSample.objects.create(
                    media_type=data['media_type'], 
                    media=upload_img_url,
                    user_id=user_obj)
                sample_serializer = WorkSampleSerializer(work_sample_obj)
                return Response({
                    "mesasge":"Work sample created successfully",
                    "work_sample":sample_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message":"Maximum worksample limit reached"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message":upload_wrk_samp_resp['message']
            }, status=status.HTTP_400_BAD_REQUEST)
        
class WorkSampleDetailView(APIView):
    permission_classes = ([IsAuthenticated])

    def get_object(self, id):
        try:
            return WorkSample.objects.get(id=id)
        except Exception as e:
            return Http404
        
    def put(self, request, id):
        work_sample_obj = self.get_object(id)
        data = request.data
        update_serializer = WorkSampleSerializer(work_sample_obj, data=data, partial=True)
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()
        serializer = WorkSampleSerializer(work_sample_obj)
        return Response({
            "message":"Work sample objects updated successfully",
            "work_sample":serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        work_sample_obj = self.get_object(id)
        work_sample_obj.delete()
        return Response({
            "message":'Work sample deleted successfully'
        }, status=status.HTTP_200_OK)