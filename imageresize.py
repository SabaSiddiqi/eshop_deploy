import django
import shutil


import sys, os
path = '/home/iyraseshop/iyraseshop'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chart_shirt.settings")
django.setup()

from shop.models import Image, ImageAlbum
from django.core.files.uploadedfile import SimpleUploadedFile
import PIL.Image as Pillow

 # for each image in images
for each_image in Image.objects.all():

    #get image file path
    dir_name = '/home/iyraseshop/iyraseshop/media'
    base_filename = 'images'
    folder_name = str(each_image.album)
    file_name = str(each_image.image)
    path_image = os.path.join(dir_name, file_name)
    print("Path Image", path_image)


    if not path_image:
        print("Path Image doesn't exist")

    else:
        print("Path Image Exists")
        #open image
        image = Pillow.open(path_image)
        width, height = image.size

        #if image is default image
        if each_image.default == True:

            #create icon images for refault

            #resize image before saving as icon
            icon_image = image.resize((256, 256))

            #set file name - album_name/image_name_icon.jpeg
            file_name = str(each_image.album) + "_icon." + str(each_image.image).split(".")[-1]

            #check image format
            image_format = str(each_image.image).split(".")[-1]
            print("Image Format",image_format)

            cond1 = image_format == 'jpg'
            cond2 = image_format == 'jpeg'


            #if format is jpeg or jpg
            if (cond1 or cond2):
                print(each_image.image, "It's a JPEG/JPG Image")

            #if format is other than jpeg convert to jpeg
            else:
                print(each_image.image, "It's a Other Image")
                # img = Pillow.open(path_image)
                # new_img = img.convert('RGB')
                # file_name = str(each_image.image).split(".")[0]+'.jpeg'
                # path_image = os.path.join(dir_name, file_name)
                # new_img.save(path_image)
                # file_name = str(each_image.album) + "_icon." + str(each_image.image).split(".")[-1]


            #file path to icon
            path_icon = os.path.join(dir_name, base_filename, str(each_image.album), 'icon', file_name)

            #directory path to icon
            image_path = os.path.join(dir_name, base_filename, str(each_image.album), 'icon')


            #check if icon folder exists
            isExist = os.path.exists(image_path)

            # if icon does not folder exists
            print("Path Icon", path_icon)
            print("File Name", file_name)

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
