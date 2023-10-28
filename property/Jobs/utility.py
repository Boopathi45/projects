from django.conf import settings
import datetime, os, shutil
from zipfile import ZipFile

def replace_file_name_space(filename):
    return filename.replace(" ", "_")

def upload_job_image(request, job_id, job_image):
    try:
        cnt = 0
        size = job_image.size
        base_path = settings.MEDIA_ROOT
        site_url =("http://{}".format(request.META['HTTP_HOST']))
        current_datetime = f"{datetime.datetime.now().strftime('%Y')}/{datetime.datetime.now().strftime('%m')}/{datetime.datetime.now().strftime('%d')}"
        media_url = f"{job_id}/{'To-Do'}"
        date_path = os.path.join(base_path, current_datetime)
        if not os.path.exists(date_path):
            os.makedirs(date_path)
        final_path = os.path.join(date_path, media_url)
        if not os.path.exists(final_path):
            os.makedirs(final_path)

        filename, mime_type = os.path.splitext(job_image.name)
        filename = replace_file_name_space(filename)
        img_mime_type = ".jpeg" if mime_type != ".png" else mime_type

        # raw_file_path = f"{final_path}/{filename}{img_mime_type}"

        # if f"{filename}{img_mime_type}" in os.listdir(final_path):
        #     cnt = cnt+1
        #     raw_file_path = f"{final_path}/{filename}-{cnt}{img_mime_type}"
        # elif f"{filename}{img_mime_type}" not in os.listdir(final_path):
        #     exts_file = glob.glob(f"{final_path}/{filename}([0-9]*).{img_mime_type}")
        #     raw_file_path = f"{final_path}/{filename}-{len(exts_file)}{img_mime_type}"
        # else:
        #     raw_file_path = f"{final_path}/{filename}{img_mime_type}"

        for file in os.listdir(final_path):
            raw_file_name, mime_type = os.path.splitext(file)
            cnt+= 1
            if raw_file_name == filename:
                raw_file_path = f'{final_path}/{filename}-{cnt}{img_mime_type}'

                # if os.path.exists(raw_file_path):
                #     exists_thumb_file_name = os.path.split(raw_file_path)
                #     thumb_file_and_ext = exists_thumb_file_name[1].split("-")
                #     cnt_and_ext = thumb_file_and_ext[1].split(".")
                #     file_cnt_number = int(cnt_and_ext[0])+1
                #     raw_file_path = f'{final_path}/{filename}-{file_cnt_number}{img_mime_type}'

        # original_path = f"{final_path}/{job_image}"

        with open (raw_file_path, mode='wb+') as file:
            for chunk in job_image.chunks():
                file.write(chunk)
            url = raw_file_path
        return ({
            "status":True,
            "url":url
        })
    except Exception as e:
        return ({
            "status":False,
            "message":str(e)
        })

def remove_job_image(obj, job_id):
    try:
        date_var = obj.strftime("%Y,%m,%d")
        date_time = date_var.replace(",","/")
        media_url = f"{job_id}"
        site_url = str(f"{settings.MEDIA_ROOT}/{date_time}/")
        for file in os.listdir(site_url):
            if file == job_id :
                path = os.path.join(site_url, media_url)
                shutil.rmtree(path, ignore_errors=True)
        return ({
            "status":True,
        })
    except Exception as e:
        return({
            "status":False,
            "message":str(e)
        })
    
def delete_image(url):
    try:
        deleted_urls = []
        for path in url:
            image = os.path.split(path['url'])
            image_name = image[1]
            media_path = path['url'].split('media')
            img_path = media_path[1].split(image_name)
            site_url = str(f"{settings.MEDIA_ROOT}{img_path[0]}")
            for file in os.listdir(site_url):
                if file == image_name:
                    url = os.path.join(site_url, file)
                    os.remove(url)
            del_resp = {"url":path['url'], "name":image_name}        
            deleted_urls.append(del_resp)
        return({
            "status":True,
            "url":deleted_urls,
            "image_name":image_name
        })
    except Exception as e:
        return({
            "status":False,
            "message":str(e)
        })
    
def storage_consumed(url):
    try:
        for path in url:
            media_count = len(url)
            image = os.path.split(path['url'])
            image_name = image[1]
            media_path = path['url'].split('media')
            img_path = media_path[1].split(image_name)
            site_url = str(f"{settings.MEDIA_ROOT}{img_path[0]}")
            for storage in os.listdir(site_url):
                file = os.path.join(site_url, storage)
                storage_size = os.path.getsize(file)
            storage_consume = {"total_files":media_count, "consumed_size":storage_size}
        return({
            "status":True,
            "storage_consume":storage_consume
        })
    except Exception as e:
        return({
            "status":False,
            "message":str(e)
        })
    
def zip_image(obj, job_id):
    try:
        print("welcome")
        date_var = obj.strftime("%Y,%m,%d")
        date_time = date_var.replace(",","/")
        media_url = f"{job_id}/{'To-Do'}"
        site_url = str(f"{settings.MEDIA_ROOT}/{date_time}/")
        for file in os.listdir(site_url):
            if file == job_id :
                zip_path = f"{site_url}{media_url}"
                with ZipFile(f"{zip_path}/{'zip_images.zip'}", 'w') as zip_object:
                    for files in os.listdir(zip_path):
                        img_file = f"{zip_path}/{files}"
                        extension = img_file.split('.')
                        if extension[1] != 'zip':
                            zip_object.write(img_file, os.path.basename(files))
        return ({
            "status":True,
            "message":"Zip file created"
        })
    except Exception as e:
        return({
            "status":False,
            "message":str(e)
        })