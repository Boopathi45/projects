import base64, subprocess, sys, os, requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from PIL.ImageFilter import BLUR
from rest_framework.response import Response
from rest_framework.decorators import APIView
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from threading import Thread
from time import sleep
from django.conf import settings

from Jobs.serializers import MultithreadtestSerializer

counter = 0

class PillowView(APIView):
    
    def get(self, request):
        path = "E:\Boopathi\Python\sample_images\python-pillow5.png"
        image = Image.open(path)
        image.show()
        image.save("E:\Boopathi\django\property\python-pillow4.png")
        image1 =Image.open("E:\Boopathi\django\property\python-pillow4.png")
        image.thumbnail((80, 80))
        image.save("E:\Boopathi\django\property\python-pillow4_thumb.png")
        thumb = Image.open("E:\Boopathi\django\property\python-pillow4_thumb.png")

        r, g, b = image.split()
        image.show()
        image = Image.merge("RGB", (b, g, r))
        image.show()
        image.show()

        blur_img = image.filter(ImageFilter.GaussianBlur(5))
        blur_img.show()
        blur_img.save("E:\Boopathi\django\property\python-pillow4_blur.png")

        crop_img = image.crop((1,2,300,300))
        crop_img.show()
        crop_img.save("E:\Boopathi\django\property\python-pillow4_crop.png")

        flip_img = image.transpose(Image.FLIP_LEFT_RIGHT)
        flip_img.show()
        flip_img.save("E:\Boopathi\django\property\python-pillow4_flip.png")

        image.resize((80,80))
        image.show()
        image.save("E:\Boopathi\django\property\python-pillow4_resize.png")

        width, height = image.size
        draw = ImageDraw.Draw(image)
        text = "Live to race"
        font = ImageFont.truetype('arial.ttf', 36)
        textwidth, textheight = draw.textsize(text, font)
        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin
        draw.text((x, y), text, font=font)
        image.save("E:\Boopathi\django\property\python-pillow4_resize.png")

        filter_img = image.filter(BLUR)
        filter_img.show()
        filter_img.save("E:\Boopathi\django\property\python_pillow4.minfilter.png")

        image.convert('RGB')
        image.filter(BLUR)
        image.show()

        draw = ImageDraw.Draw(image)
        draw.line((0, 0) + image.size, fill=200)
        draw.line((0, image.size[1], image.size[0], 0), fill=128)
        image.show()
        image.save("E:\Boopathi\django\property\python_pillow4_line.png")

        img = Image.new('RGB', (500, 300), (125, 125, 125))
        draw = ImageDraw.Draw(img)
        draw.line((100, 100, 300, 100), fill=(0, 0, 0), width=10)
        img.show()

        return Response({ 
            "success"
        })

class Base64(APIView):

    def get(self, request):
        try:
            with open("E:\Boopathi\django\property\python-pillow4_flip.png", mode="rb") as image_file:
                binary_file = base64.b64encode(image_file.read())
            with open("E:\Boopathi\django\property\image_str.bin", mode="wb") as bin_file:
                bin_file.write(binary_file)
            return Response({
                "message":"Converted successfully"
            })
        except Exception as e:
            return Response({
                "message":str(e)
            })

    def post(self, request):
        try:
            with open("E:\Boopathi\django\property\image_str.bin", mode="rb") as bin_file:
                image_file = base64.b64decode(bin_file.read())

            with open("E:\Boopathi\django\property\str_img.png", mode="wb") as img_file:
                img_file.write(image_file)
            return Response({
                    "message":"Converted successfully"
                })
        except Exception as e:
            return Response({
                "message":str(e)
            })
        
class SubProcesses(APIView):

    def get(self, request):
        process = subprocess.run(["python", "check_python_file.py"], capture_output=True, text=True, check=False)
        
        process = subprocess.run(["E:\Boopathi\django\property\jobs\pillow", "-c", "print('This is sample subprocess function output')"], capture_output=True, text=True)
        
        p = subprocess.Popen(["python", "python_file.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = p.communicate()
        print(output)

        return_code = subprocess.call(["python", "--version"])
        if return_code == 0:
            print("Code executed successfully")
        else:
            print("Code executed with some error having" + return_code)

        input = subprocess.Popen(["python", "python_file.py"], stdout = subprocess.PIPE, text=True)
        print(input)
        input1 = subprocess.Popen(["grep", "sample"], stdin=input.stdout, stdout=subprocess.PIPE, text=True)
        output, error = input1.communicate()
        print(output)
        print(error)

        process1 = subprocess.run([sys.executable, '-c', "print('This is the sample subprocess')"], text=True)
        print(process1)
        process = subprocess.run(["python","manage","shell", '-c', "print('This is the sample subprocess')"], text=True, shell=True)
        print(process.stdout)

        input = subprocess.run(["python", "E:/Boopathi/django/property/jobs/python_file.py"], capture_output=True, text=True)
        print(input.stdout)
        print(input.stderr)

        return Response({
            "success"
        })  
    
class MultithreadingPractice(APIView):
    
    def increase(by): 
        global counter
        local_counter = counter
        local_counter += by

        sleep(0.1)

        counter = local_counter
        print(f"The counter={counter}")

    def square(num):
        val = num*num
        print(f"Square of {num} is {val}")

    def post(self, request):
        serializer = MultithreadtestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        img_file = serializer.validated_data.get('img_file')
        base_path = settings.MEDIA_ROOT
        file_upload_path = f"{base_path}/upload/{img_file.name}"
        if not os.path.exists(file_upload_path):
            os.makedirs(file_upload_path)
        with open (file_upload_path, mode='wb') as file:
            for chunk in img_file.chunks():
                file.write(chunk)
            url = file_upload_path
            print(url)
        return Response({
        "message":"Success"
        })

    def get(self, request):
        # img_file = "E:/Boopathi/Python/sample_images/resized_sample_images/1.jpg"
        file_name_from_dir = []
        file_directory = "E:/Boopathi/Python/sample_images/resized_sample_images"
        for files in os.listdir(file_directory):
            file_name_from_dir.append(files)
        threads = []
        for file in file_name_from_dir:
            t1 = Thread(target=self.upload, args=(file))
            threads.append(t1)
            t1.start()
        for thread in threads:
            thread.join()

        print("The final counter is {}".format(counter))  
        return Response({
        "message":"Success"
        })
      
# class DownloadImage(APIView):
#     img_path = "https://www.lamborghini.com/sites/it-en/files/DAM/lamborghini/facelift_2019/homepage/families-gallery/2022/04_12/family_chooser_tecnica_m.png"
#     data = requests.get(img_path)
#     download_path = 'E:/Boopathi/Python/sample_images/resized_sample_images/file1.jpg'
#     with open(download_path, 'wb') as f:
#         f.write(data.content)
#         f.close()
#     image = Image.open(download_path)
#     image.show()

    # def post(self, request):
    #     url = request.data.get("url")
    #     response = requests.get(url)
    #     image_name = url.split("To_Do/")[1]
    #     download_image_path = f'media/download_images/{image_name}'
    #     with open(download_image_path, "wb") as f:
    #         f.write(response.content)