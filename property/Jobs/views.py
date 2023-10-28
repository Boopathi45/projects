from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
import csv, xlsxwriter, io, subprocess, sys

from Accounts.models import User
from Jobs.models import *
from Jobs.serializers import *
from Jobs.utility import *
from Settings.models import MasterTurnAroundTime
from services.models import Services, ServiceEditingPreference

class JobLists(APIView):
    
    parser_classes = ([JSONParser, FormParser, MultiPartParser])
    permission_classes = ([IsAuthenticated])
    
    def get(self, request):
        total_jobs = Job.objects.all()
        serializer = JobSerializer(total_jobs, many=True)
        return Response({
            "message":"Jobs details fetched successfully",
            "jobs":serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user_obj = User.objects.get(id=request.user.id)
        serializer = CreateJobSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        ser_lst, pre_lst, items, net_price = [], [], [], 0
        image_count = len(data['media_url'])
        master_obj = MasterTurnAroundTime.objects.filter(id=data['turn_around_time']).first()
        master_duration = master_obj.duration
        storage_consumed_resp = storage_consumed(data['media_url'])
        if storage_consumed_resp['status'] == True:
            services_obj = Services.objects.filter(id__in=data['services_lst'])
            if services_obj:
                for service in services_obj:
                    ser_lst.append({'id':service.id, 'name':service.name})
                    items.append({
                        "title":service.name, 
                        "item_price":service.price, 
                        "file_count":image_count,  
                        "item_total":image_count*service.price, 
                        "item_type":"service"
                        }
                    )
                    net_price = net_price + image_count*service.price
            else:
                return Response({
                    "message":"Services does not exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            prefernces_obj = ServiceEditingPreference.objects.filter(preference_id__in=data['preferences_lst'])
            if prefernces_obj:
                for preference in prefernces_obj:
                    pre_lst.append({'id':preference.id, 'name':preference.preference_id.name})
                    items.append({
                        "title":preference.preference_id.name, 
                        "item_price":preference.price, 
                        "file_count":image_count, 
                        "item_total":image_count*preference.price, 
                        "item_type":"base preferences"
                        }
                    )
                    net_price = net_price + image_count*preference.price
            else:
                return Response({
                    "message":"Editing preference does not exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            turn_around_time_obj = MasterTurnAroundTime.objects.filter(id=data['turn_around_time']).first()
            if turn_around_time_obj:
                items.append({
                    "title":f"Turn around time ({turn_around_time_obj.duration}Hrs)", 
                    "item_price":turn_around_time_obj.price, 
                    "file_count":image_count, 
                    "item_total":image_count*turn_around_time_obj.price, 
                    "item_type":"turn around time"
                    }
                )
                net_price = net_price + image_count*turn_around_time_obj.price
            else:
                return Response({
                    "message":"Turn around time does not exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            # job_summary = [frozenset(d.items()) for d in items]
            # exists_summary = [frozenset(d.items()) for d in data['summary']['items']]
            status_obj = JobStatus.objects.filter(status_id=1).first()
            if items == data['summary']['items']:
                job_obj = Job.objects.create(
                    job_id=data['job_id'], 
                    title=data['title'], 
                    turn_around_time=master_duration, 
                    media=data['media_url'], 
                    storage_consumed=storage_consumed_resp['storage_consume'], 
                    user_id=user_obj, 
                    preferences_lst=pre_lst, 
                    services_lst=ser_lst, 
                    gross_price=net_price, 
                    net_price=net_price,
                    status=status_obj
                    )
                job_serializer = JobSerializer(job_obj)
                JobPayment.objects.create(
                    item_list=data['summary']['items'], 
                    gross_price=net_price, 
                    net_price=net_price, 
                    job_id=job_obj, 
                    user_id=user_obj
                    )
                return Response({
                    "message":"Job created successfully",
                    "item":items,
                    "job":job_serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message":"Unmatched recoreds.. unable to create job"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message":storage_consumed_resp['message']
            }, status=status.HTTP_400_BAD_REQUEST)

class RawImageUpload(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        serializer = RawImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        job_image = data.get('job_image')
        job_id = data.get('job_id')
        upload_job_image_resp = upload_job_image(request, job_id, job_image)
        if upload_job_image_resp['status'] == True:
            media_url_resp = {"url":upload_job_image_resp['url'], "name":job_image.name}
            media_lst = []
            if not media_url_resp in media_lst:
                media_lst.append(media_url_resp)
            else:
                return Response({
                    "message":"Image already exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                    "message":"Raw image uploaded successfully",
                    "media_url":media_lst
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message":upload_job_image_resp['message'],
            }, status=status.HTTP_400_BAD_REQUEST)

class JobDetails(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        data = request.data
        delete_serializer = JobImageDeleteSerializer(data=data)
        delete_serializer.is_valid(raise_exception=True)
        data = delete_serializer.data
        job_obj = Job.objects.filter(job_id=data.get('job_id'), user_id=request.user.id).first()
        job_del_path = remove_job_image(job_obj.created_on, data.get('job_id'))
        if job_del_path['status'] == True:
            job_obj.media = None
            job_obj.save()
            return Response({
                "message":"Job image deleted successfully"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message":job_del_path['message'],
            }, status=status.HTTP_400_BAD_REQUEST)
        
class JobImageDeleteView(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        data = request.data
        serializer = ImageDeleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        job_obj = Job.objects.filter(job_id=data.get('job_id'), user_id=request.user.id).first()
        del_path = delete_image(data.get('image_url'))
        if del_path['status'] == True:
            media_path = job_obj.media
            delete_resp = del_path['url']
            for del_file_url in delete_resp:
                if del_file_url in media_path:
                    media_path.remove(del_file_url)
                    job_obj.save()
                else:
                    return Response({
                        "message":"Path does not exists"
                    }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                    "message":"Image url removed successfully"
                }, status.HTTP_200_OK)
        else:
            return Response({
                "message":del_path['message'],
            }, status=status.HTTP_400_BAD_REQUEST)
        
class JobSummaryView(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        data = request.data
        serializer = JobSummarySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        items = []
        net_price = 0
        image_count = int(data['image_count'])
        services_obj = Services.objects.filter(id__in=data['services_lst'])
        if services_obj:
            for service in services_obj:
                items.append({
                    "title":service.name, 
                    "item_price":service.price, 
                    "file_count":image_count,  
                    "item_total":image_count*service.price, 
                    "item_type":"service"
                    }
                )
                net_price = net_price + image_count*service.price
        else:
            return Response({
                "message":"Services does not exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        prefernces_obj = ServiceEditingPreference.objects.filter(preference_id__in=data['preferences_lst'])
        if prefernces_obj:
            for preference in prefernces_obj:
                items.append({
                    "title":preference.preference_id.name, 
                    "item_price":preference.price, 
                    "file_count":image_count, 
                    "item_total":image_count*preference.price, 
                    "item_type":"base preferences"
                    }
                )
                net_price = net_price + image_count*preference.price
        else:
            return Response({
                "message":"Editing preference does not exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        turn_around_time_obj = MasterTurnAroundTime.objects.filter(id=data['turn_around_time']).first()
        if turn_around_time_obj:
            items.append({
                "title":f"Turn around time ({turn_around_time_obj.duration}Hrs)", 
                "item_price":turn_around_time_obj.price, 
                "file_count":image_count, 
                "item_total":image_count*turn_around_time_obj.price, 
                "item_type":"turn around time"
                }
            )
            net_price = net_price + image_count*turn_around_time_obj.price
        else:
            return Response({
                "message":"Turn around time does not exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message":"Job summary details fetched successfully",
            "summary":{
                "items":items,
                "gross_price":net_price,
                "net_price":net_price
            },
        }, status=status.HTTP_200_OK)
    
class DashboardJobStatus(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        orders = Job.objects.all().count()
        in_progress = Job.objects.filter(status=2).count()
        completed = Job.objects.filter(status=3).count()
        return Response({
            "message":"Details fetched successfully",
            "orders": orders,
            "in_progress": in_progress,
            "completed": completed
        }, status.HTTP_200_OK)
    
class GenerateInvoicePdf(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request, id):
        Job_details = Job.objects.values().get(pk=id)
        template_path = 'Jobs/generate_pdf.html'
        context = {"Job_details": Job_details}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{Job_details}.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF( html, dest=response)
        if pisa_status.err:
            HttpResponse('We had some errors <pre>' + html + '</pre>') 
        return response
    
class GenerateInvoiceCsv(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request, id):
        user_obj = User.objects.get(id=request.user.id)
        response = HttpResponse(content_type='text/csv')  
        response['Content-Disposition'] = 'attachment; filename="sample_csv.csv"'
        writer = csv.writer(response) 
        s_no = 1
        if not user_obj.is_admin: 
            Job_info = Job.objects.get(id=id)
            writer.writerow(["S.NO", "JOB NAME", "ORDER ID", "TOTAL FILES", "DATE", "PRICE",])  
            writer.writerow([s_no, Job_info.title, Job_info.id, Job_info.storage_consumed['total_files'], Job_info.created_on, Job_info.net_price])
            s_no = s_no+1
        else:
            Job_info = Job.objects.all()
            writer.writerow(["S.NO", "JOB NAME", "ORDER ID","TOTAL FILES", "DATE","PRICE"])  
            for jobs in Job_info:
                writer.writerow([s_no, jobs.title, jobs.id, jobs.storage_consumed['total_files'], jobs.created_on, jobs.net_price])
                s_no = s_no+1
        return response
    
class GenerateInvoiceXlsx(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request, id):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'remove_timezone': True})
        worksheet = workbook.add_worksheet('Job_details')
        bold = workbook.add_format({'bold': True})
        row, col, s_no = 1, 0, 1
        job_info = Job.objects.all()
        worksheet.write('A1', 'S_NO', bold)
        worksheet.write('B1', 'JOB_NAME', bold)
        worksheet.write('C1', 'ORDER_ID', bold)
        worksheet.write('D1', 'TOTAL_FILES', bold)
        worksheet.write('E1', 'DATE', bold)
        worksheet.write('F1', 'PRICE', bold)
        for jobs in job_info:
            worksheet.write(row, col, s_no)
            worksheet.write(row, col + 1, jobs.title)
            worksheet.write(row, col + 2, jobs.id)
            worksheet.write(row, col + 3, jobs.storage_consumed['total_files'])
            worksheet.write(row, col + 4, jobs.created_on.strftime("%B %d, %Y %I:%M %p"))
            worksheet.write(row, col + 5, jobs.net_price)
            row += 1
            s_no = s_no + 1
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=sample_xlsx.xlsx"
        return response
    
class ZipImage(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        job_id = request.data.get('job_id')
        job_obj = Job.objects.get(job_id=job_id)
        if job_obj:
            zip_img_resp = zip_image(job_obj.created_on, job_id)
            if zip_img_resp['status'] == True:
                return Response({
                    "message":zip_img_resp['message']
                }, status.HTTP_200_OK)
            else:
                return Response({
                    "message":zip_img_resp['message']
                }, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message":"Job id is required"
            }, status.HTTP_400_BAD_REQUEST)
        
class CompleteJobImages(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        job_id = request.data.get('job_id')