from django.shortcuts import render, redirect
from .models import Profile
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

# email

from django.core.mail import EmailMultiAlternatives, EmailMessage,send_mail

# Create your views here.


def accept(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        summary = request.POST.get("summary")
        degree = request.POST.get("degree")
        school = request.POST.get("school")
        university = request.POST.get("university")
        previouswork = request.POST.get("previouswork")
        skills = request.POST.get("skills")

        profile = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree,
                          school=school, university=university, previouswork=previouswork, skills=skills)
        profile.save()

    return render(request, 'pdf/accept.html')


def intro(request):
    profile = Profile.objects.all()
    return render(request, 'pdf/intro.html', {"profile": profile})


def resume(request, id):
    user_details = Profile.objects.get(pk=id)
    template_path = 'pdf/resume.html'
    context = {"user_details": user_details}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user_details}.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF( html, dest=response, link_callback='pdf/intro-page' )
    print(type(pisa_status))

    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>') 
    
    # msg = EmailMessage('testing', 'Sample pdf', 'boopathimuthu2001@gmail.com', ['boopathi.m@osoftz.com'])
    # msg.content_subtype = "html"  
    # msg.attach_file(f"Downloads/{user_details}")
    # msg.send()

    send_mail('Sample_subject', message=f'Dear, Mr.{user_details}, Your resume generated successfully', from_email='boopathimuthu2001@gmail.com', recipient_list=['boopathi.m@osoftz.com'])

    return response

def lists(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/lists.html', {"profiles": profiles})
