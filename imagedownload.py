import django
import shutil
from django.core.files import File
from PIL import Image
import PIL
import requests
from io import BytesIO
from resizeimage import resizeimage
import PIL.Image as Pillow

import sys, os, requests
import urllib.request

path = '/home/iyraseshop/iyraseshop'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chart_shirt.settings")
django.setup()

from shop.models import Image, ImageAlbum
from django.core.files.uploadedfile import SimpleUploadedFile

def trunc_at(s, d, n=2):
    "Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d."
    return d.join(s.split(d, n)[:n])

def create_icon_image(each_image, width, height):
    dir_name = '/Users/sabasiddiqi/Desktop/eshop_24aug2022/eshop_deploy/media/'
    base_filename = 'images'
    folder_name = str(each_image.album)
    file_name = str(each_image.image)
    path_image = os.path.join(dir_name, file_name)

    if not path_image:
        print("Path Image doesn't exist")

    else:
        print("Path Image Exists")
        image = Pillow.open(path_image)

        #if image is default image
        if each_image.default == True:

            #create icon images for refault

            #resize image before saving as icon
            icon_image = image.resize((height, width))

            #set file name - album_name/image_name_icon.jpeg
            file_name = str(each_image.album) + "_icon." + str(each_image.image).split(".")[-1]

            #check image format
            image_format = str(each_image.image).split(".")[-1]

            cond1 = image_format == 'jpg'
            cond2 = image_format == 'jpeg'

            #file path to icon
            path_icon = os.path.join(dir_name, base_filename, str(each_image.album), 'icon', file_name)

            #directory path to icon
            image_path = os.path.join(dir_name, base_filename, str(each_image.album), 'icon')

            #check if icon folder exists
            isExist = os.path.exists(image_path)

            if not isExist:
                # create icon folder
                print("Does Not Exist")
                os.makedirs(os.path.join(dir_name, base_filename, str(each_image.album), 'icon'))
                print(path_icon)
                icon_image.save(path_icon)
                each_image.icon_image = SimpleUploadedFile(name=file_name, content=open(path_icon, 'rb').read(), content_type='image/jpeg')
                os.remove(path_icon)
                each_image.save()
            else:
                print("Exist")
                shutil.rmtree(image_path)
                os.makedirs(os.path.join(dir_name, base_filename, str(each_image.album), 'icon'))
                icon_image.save(path_icon)
                each_image.icon_image = SimpleUploadedFile(name=file_name, content=open(path_icon, 'rb').read(), content_type='image/jpeg')
                os.remove(path_icon)
            each_image.save()


image_url = 'https://www.cartersoshkosh.ca/on/demandware.static/-/Sites-carters_master_catalog/default/dw4b951e14/productimages/1P569010.jpg'
image_name = '101_13.jpg'
temp_name = 'temp_image.jpg'

try:
    album_name = ImageAlbum.objects.get(name=trunc_at(str(image_name).split('.')[0],'_'))

except:
    album_name = ImageAlbum.objects.create(name=trunc_at(str(image_name).split('.')[0],'_'))

fd = urllib.request.urlretrieve(image_url,temp_name)
im1 = PIL.Image.open(temp_name)
img = resizeimage.resize_contain(im1, [600,600], bg_color=(250, 250, 250, 0))
img = img.convert('RGB')
img.save('temp_image.jpg')

dir_name = '/Users/sabasiddiqi/Desktop/eshop_24aug2022/eshop_deploy/'
path_image = os.path.join(dir_name, temp_name)


from django.core.files.base import ContentFile
a = Image.objects.create(
    name=str(image_name).split('.')[0],
    # image=File(filename),
    image=SimpleUploadedFile(name=image_name, content=open(path_image, 'rb').read(), content_type='image/jpeg'),
    default=True,
    album=album_name,
    )
create_icon_image(a, 256, 256)
