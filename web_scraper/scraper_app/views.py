from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from .models import Links
from django.http import HttpResponseRedirect

# Create your views here.


def intro(request):
    return render(request,'scraper_app/intro_page.html')

def scrape(request):

    if request.method =="POST":
        site = request.POST.get('site'," ")
        
        page = requests.get(site)    # Requests --- To requests http links from the website
        soup = BeautifulSoup(page.text,'html.parser')    # BeautifulSoup --- to align the links properly for the right view
        
        for links in soup.find_all('a'):
            link_address = links.get('href')
            link_text = links.string
            Links.objects.create( address = link_address , name = link_text)
        return HttpResponseRedirect('/lists')
    
    else:
        data = Links.objects.all()

    return render(request,'scraper_app/lists.html',{"data":data})
    
def delete(request):
    Links.objects.all().delete()
    return HttpResponseRedirect('/lists')

def del_config(request):
    return render(request,'scraper_app/del_config.html')
