from django.urls import path

from Jobs.views import *
from Jobs.pillow import *

appname = 'Jobs'

urlpatterns = [
    path('list/', JobLists.as_view()),
    path('details/', JobDetails.as_view()),
    path('upload_images/', RawImageUpload.as_view()),
    path('job_image_delete/', JobImageDeleteView.as_view()),    
    path('summary/', JobSummaryView.as_view()),
    path('dashboard_status/', DashboardJobStatus.as_view()),
    path('pillow/', PillowView.as_view()),
    path('zip_image/', ZipImage.as_view()),
    path('img_to_str/', Base64.as_view()),
    path('sub_process/', SubProcesses.as_view()),
    path('complete_job_images/', CompleteJobImages.as_view()),
    path('multithreading/', MultithreadingPractice.as_view()),
    # path('download_image/', DownloadImage.as_view()),

    # -- invoices url --    

    path('generate_invoice_pdf/<int:id>', GenerateInvoicePdf.as_view()),
    path('generate_invoice_csv/<int:id>', GenerateInvoiceCsv.as_view()),
    path('generate_invoice_xlsx/<int:id>', GenerateInvoiceXlsx.as_view()),
]