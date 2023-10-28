from django.shortcuts import render
from jwt_project import settings
import os.path

# email creation
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# zip file generation
from zipfile import ZipFile, ZIP_DEFLATED
import os
import pathlib

appname = 'mail'


def sendSimpleEmail(request):
    subject = 'creation of the email demonstration'
    message = 'sample message'
    email_from = 'osoftzweb@gmail.com'
    recipient = ['boopathi.m@osoftz.com']
    send_mail(subject, message, email_from, recipient)
    return HttpResponse(' email send successfully ')

# --------------------


def samplehtmlemailview(request):
    context = {
        'message': 'sample email message'
    }
    html_message = render_to_string('mail/sample_email.html', context)
    text_message = strip_tags(html_message)
    email = EmailMultiAlternatives(
        'Sample email',
        text_message,
        'boopathiboopathi30738@gmail.com',
        ['boopathi.m@osoftz.com'],
    )
    email.content_subtype = 'html'  # to specify the html file
    email.attach_alternative(html_message, "text/html")   # format
    email.send()
    return HttpResponse("Success")

# -------------------


def zipmailview(request):

    if request.method == 'GET':
        return render(request, 'mail/zip.html')

    elif request.method == 'POST':
        base_path = settings.MEDIA_ROOT
        subject = request.POST.get('sub')
        name = request.POST.get('name')
        email_from = str(request.POST.get('sender'))
        to = request.POST.get('receiver')
        file_name = request.POST.get('filename')
        uploaded_image = request.FILES.getlist('uploaded_img')

        for image in uploaded_image:
            original_path = f"{base_path}\{str(image)}"
            with open(original_path, mode='wb') as file:
                for chunk in image.chunks():
                    file.write(chunk)

        zip_path = f'{base_path}\{file_name}.zip'
        directory_to_zip = base_path
        folder = pathlib.Path(directory_to_zip)

        with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zip:
            for file in folder.iterdir():
                print(file)
                file_extension = pathlib.Path(file).suffix
                if file_extension != '.zip':
                    print("Zip file created successfully")
                    os.remove(file)
                else:
                    pass

    send_attachment(request, subject, email_from, to, file_name)
    return HttpResponse('E-mail sent successfully')


def send_attachment(request, subject, email_from, to, file_name):

    body = f"sample mail attachment"
    message = MIMEMultipart()
    message['from'] = email_from
    message['to'] = to
    message['subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    filename = f'E:\Boopathi\django\jwt_project\media\zip_images\{file_name}.zip'
    attachment = open(filename, 'rb')
    # encode as base 64
    attachment_package = MIMEBase('application', 'octet_stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header(
        'Content-Disposition', f'attachment; filename={file_name}.zip')
    message.attach(attachment_package)
    text = message.as_string()
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.connect(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(message['from'], message['to'], text)
    print('Mail send successfully')
    server.quit()

    return HttpResponse('Attchment send successfully')
