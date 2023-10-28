from django.conf import settings
import os

from property import settings

def upload_work_sample(request, images, id):
    try:
        base_path = settings.MEDIA_ROOT
        site_url =("http://{}".format(request.META['HTTP_HOST']))
        sample_path = f"{base_path}/{'work_sample'}"
        if not os.path.exists(sample_path):
            os.makedirs(sample_path)
        id_path = f"{sample_path}/{id}"
        if not os.path.exists(id_path):
            os.makedirs(id_path)
        img_path = os.path.join(f"{id_path}/{'images'}")
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        file_path = os.path.join(f"{img_path}/{images}")
        with open(file_path, mode='wb') as file:
            for chunk in images.chunks():
                file.write(chunk)
            url = f"{site_url}{settings.MEDIA_URL}{'work_sample'}/{id}/{'images'}/{images}"
        return({
            "status":True,
            "url":url
        })
    except Exception as e:
        return({
            "status":False,
            "message":str(e)
        })