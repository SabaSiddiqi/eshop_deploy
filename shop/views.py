from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from shop.models import *
from django.contrib.auth.decorators import login_required
from guest_user.decorators import allow_guest_user
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.db.models import Sum
from django.core.mail import send_mail, BadHeaderError
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from django.template.loader import render_to_string, get_template
from django.core.files import File
from datetime import date
from datetime import datetime
import os
from shop.models import Image, ImageAlbum, Attribute
from django.core.files.uploadedfile import SimpleUploadedFile
import PIL
import PIL.Image as Pillow
import shutil
from resizeimage import resizeimage
import urllib.request

def show_images(request):

    image_dict = {}

    for each_album in ImageAlbum.objects.all():
        image_dict[each_album]= Image.objects.filter(album = each_album)

    context={
        'images': image_dict,
        }

    return render(request, 'app/showimages.html', context)

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

def trunc_at(s, d, n=2):
    "Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d."
    return d.join(s.split(d, n)[:n])

@staff_member_required
def product_image_upload(request):

    if request.method == 'POST':
        if request.FILES is None:
            # print("No files uploaded")
            pass
        else:

            file = request.FILES
            filename = request.FILES['file']
            print(file, filename)
            album = ImageAlbum.objects.filter(name=trunc_at(str(filename),'_'))
            if album.first():
                pass
            else:
                ImageAlbum.objects.create(name=trunc_at(str(filename),'_'))

            album_name = ImageAlbum.objects.get(name=trunc_at(str(filename),'_'))
            b=str(filename).split('.')[0].split('_')[2]

            if b =='1':
                Image.objects.create(name=str(filename).split('.')[0], image=File(filename), default=True, album=album_name)
            else:
                Image.objects.create(name=str(filename).split('.')[0], image=File(filename), default=False, album=album_name)

    context={

        'categories': Category.objects.all(),
        'image_album':ImageAlbum.objects.all(),
        'all_brands':Brand.objects.all(),

        }

    return render(request, 'app/form_upload.html')

@staff_member_required
def product_add(request):
    if request.method == 'POST':

        if request.POST.get("product_name"):
            product_name = request.POST.get("product_name")

        if request.POST.get("product_desc"):
            product_desc = request.POST.get("product_desc")

        if request.POST.get("category"):
            category = request.POST.get("category")
            category = Category.objects.get(cat_name=category)

        if request.POST.get("shipment"):
            shipment = int(request.POST.get("shipment"))

        if request.POST.get("buy_price"):
            buy_price = float(request.POST.get("buy_price"))

        if request.POST.get("price"):
            price = int(request.POST.get("price"))

        if request.POST.get("apply_discount"):
            apply_discount = bool(request.POST.get("apply_discount"))

        if request.POST.get("discount_percent"):
            discount_percent = int(request.POST.get("discount_percent"))

        if request.POST.get("discount_price"):
            discount_price = int(request.POST.get("discount_price"))

        if request.POST.get("brand"):
            brand = request.POST.get("brand")
            brand=Brand.objects.get(brand_name=brand)

        if request.POST.get("variant"):
            variant = request.POST.getlist("variant")

        if request.POST.getlist("quantity"):
            quantity = request.POST.getlist("quantity")
            print("Quan: ", quantity)

        if request.POST.get("image_album"):
            image_album_name = request.POST.get("image_album")
            album_name=ImageAlbum.objects.get(name=image_album_name)

        if request.POST.get("url"):
            image_url = request.POST.get("url")
            print("Image URL", image_url)

        if request.POST.get("image_name"):
            image_name = request.POST.get("image_name")
            print("Image NAme", image_name)

        if request.POST.get("featured"):
            featured = bool(request.POST.get("featured"))

        if request.POST.get("preorder"):
            preorder = bool(request.POST.get("preorder"))

        if request.POST.get("publish"):
            publish = bool(request.POST.get("publish"))

        if request.POST.get("delivery_time"):
            delivery_time = request.POST.get("delivery_time")

        if request.POST.get("url") and request.POST.get("image_name"):
            print("Image URL", image_url)
            import urllib.request
            try:
                album_name = ImageAlbum.objects.get(name=trunc_at(str(image_name),'_'))

            except:
                album_name = ImageAlbum.objects.create(name=trunc_at(str(image_name),'_'))

            img = urllib.request.urlretrieve(image_url,image_name)


            # icon_name = str(album_name) + "_icon." + str(image_name).split(".")[-1]
            a = Image.objects.create(
                name=str(image_name).split('.')[0],
                image=File(open(img[0], 'rb')),
                default=True,
                album=album_name,
                )

            create_icon_image(a, 256, 192)

        #Add Product
        n = Product.objects.create(
            product_name=product_name,
            product_desc=product_desc,
            category=category,
            price=price,
            apply_discount=apply_discount,
            discount_percent=discount_percent,
            discounted_price=discount_price,
            brand=brand,
            publish_date=date.today(),
            image=album_name,
            is_featured=featured,
            is_published=publish,
            is_preorder=preorder,
            )

        n.save()

        for i in range(len(variant)):
            each_variant=variant[i]
            each_quantity=int(quantity[i])
            ProductVariant.objects.create(
            variant = Product.objects.get(product_id=n.pk),
            attribute = Attribute.objects.get(attribute=each_variant, attribute_category=category),
            delivery_time = DeliveryTime.objects.get(delivery_time=delivery_time),
            buy_price = buy_price,
            price = price,
            shipment = Shipment.objects.get(shipment=shipment),
            apply_discount = apply_discount,
            discount_percent = discount_percent,
            discounted_price = discount_price,
            num_available=each_quantity)

        return redirect('shop:admindash')

    context={

        'categories': Category.objects.all(),
        'image_album':ImageAlbum.objects.all(),
        'all_brands':Brand.objects.all(),
        'shipments':Shipment.objects.all(),
        'attributes':Attribute.objects.all(),
        'delivery_time':DeliveryTime.objects.all()

        }

    return render(request, 'app/add_product.html',context)

# @staff_member_required
# def main_orders_summary(request):
#     context={

#         'categories': Category.objects.all(),
#         'image_album':ImageAlbum.objects.all(),
#         'all_brands':Brand.objects.all(),
#         'shipments':Shipment.objects.all(),
#         'attributes':Attribute.objects.all(),
#         'delivery_time':DeliveryTime.objects.all(),
#         # 'mainorder': MainOrder.objects.all(),

#         }

#     return render(request, 'app/main_orders_summary.html',context)


@staff_member_required
def inventory_add(request):
    if request.method == 'POST':

        # if request.POST.get("mainorder"):
        #     mainorder = request.POST.get("mainorder")

        if request.POST.get("product_name"):
            product_name = request.POST.get("product_name")

        if request.POST.get("product_desc"):
            product_desc = request.POST.get("product_desc")

        if request.POST.get("category"):
            category = request.POST.get("category")
            category = Category.objects.get(cat_name=category)

        if request.POST.get("shipment"):
            shipment = int(request.POST.get("shipment"))

        if request.POST.get("buy_price"):
            buy_price = float(request.POST.get("buy_price"))

        if request.POST.get("price"):
            price = int(request.POST.get("price"))

        if request.POST.get("apply_discount"):
            apply_discount = bool(request.POST.get("apply_discount"))

        if request.POST.get("discount_percent"):
            discount_percent = int(request.POST.get("discount_percent"))

        if request.POST.get("discount_price"):
            discount_price = int(request.POST.get("discount_price"))

        if request.POST.get("brand"):
            brand = request.POST.get("brand")
            brand = Brand.objects.get(brand_name=brand)

        if request.POST.get("variant"):
            variant = request.POST.getlist("variant")

        if request.POST.getlist("quantity"):
            quantity = request.POST.getlist("quantity")
            print("Quan: ", quantity)

        if request.POST.get("image_album"):
            image_album_name = request.POST.get("image_album")
            album_name=ImageAlbum.objects.get(name=image_album_name)
            print("Image_Album", album_name)

        if request.POST.get("url"):
            image_url = request.POST.get("url")
            print("Image URL", image_url)

        if request.POST.get("image_name"):
            image_name = request.POST.get("image_name")
            print("Image NAme", image_name)

        if request.POST.get("featured"):
            featured = bool(request.POST.get("featured"))

        if request.POST.get("preorder"):
            preorder = bool(request.POST.get("preorder"))

        if request.POST.get("delivery_time"):
            delivery_time = request.POST.get("delivery_time")


        if request.POST.get("url") and request.POST.get("image_name"):

            image_url = request.POST.get("url")
            image_name = request.POST.get("image_name")
            temp_name = 'temp_image.jpg'

            try:
                album_name = ImageAlbum.objects.get(name=trunc_at(str(image_name).split('.')[0],'_'))

            except:
                album_name = ImageAlbum.objects.create(name=trunc_at(str(image_name).split('.')[0],'_'))

            from PIL import Image, ImageOps
            fd = urllib.request.urlretrieve(image_url,temp_name)
            im1 = PIL.Image.open(temp_name)
            # img = ImageOps.pad(im1, [600,600], color='#ffffff')
            img = ImageOps.pad(im1, (600,600), color='white')
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

        #Add Product
        n = Product.objects.create(
            product_name=product_name,
            product_desc=product_desc,
            category=category,
            # price=price,
            # apply_discount=apply_discount,
            # discount_percent=discount_percent,
            # discounted_price=discount_price,
            brand=brand,
            publish_date=date.today(),
            image=album_name,
            # is_featured=featured,
            is_published=False,
            # is_preorder=preorder,
            )

        n.save()
        # print("Main Order",mainorder)
        for i in range(len(variant)):
            each_variant=variant[i]
            each_quantity=int(quantity[i])
            ProductVariant.objects.create(
            # main_order = MainOrder.objects.get(order_number=mainorder),
            variant = Product.objects.get(product_id=n.pk),
            attribute = Attribute.objects.get(attribute=each_variant, attribute_category=category),
            # delivery_time = DeliveryTime.objects.get(delivery_time=delivery_time),
            buy_price = buy_price,
            # price = price,
            shipment = Shipment.objects.get(shipment=shipment),
            # apply_discount = apply_discount,
            # discount_percent = discount_percent,
            # discounted_price = discount_price,
            num_available=each_quantity)

        return redirect('shop:admindash')

    context={

        'categories': Category.objects.all(),
        'image_album':ImageAlbum.objects.all(),
        'all_brands':Brand.objects.all(),
        'shipments':Shipment.objects.all(),
        'attributes':Attribute.objects.all(),
        'delivery_time':DeliveryTime.objects.all(),
        # 'mainorder': MainOrder.objects.all(),

        }

    return render(request, 'app/add_inventory.html',context)

@staff_member_required
def product_update(request, product_id):
    # print(list(request.POST.items()))

    product = Product.objects.get(product_id = product_id)
    variants = ProductVariant.objects.filter( variant = product.product_id)

    #if post -> update the form

    if request.method == 'POST':

        if request.POST.get("product_name"):
            product_name = request.POST.get("product_name")
            product.product_name = product_name

        if request.POST.get("product_desc"):
            product_desc = request.POST.get("product_desc")
            product.product_desc = product_desc

        if request.POST.get("category"):
            category = request.POST.get("category")
            category = Category.objects.get(cat_name=category)
            product.category = category

        if request.POST.get("image_album"):
            image_album_name = request.POST.get("image_album")
            image_album=ImageAlbum.objects.get(name=image_album_name)
            product.image = image_album

        if request.POST.get("brand"):
            brand = request.POST.get("brand")
            brand=Brand.objects.get(brand_name=brand)
            product.brand = brand

        if request.POST.get("add_tags"):
            tag = request.POST.get("add_tags")
            product.product_tags.add(tag)

        if request.POST.get("remove_tags"):
            tag = request.POST.get("remove_tags")
            product.product_tags.remove(tag)

        product.save()

        for each_variant in variants:

            if request.POST.get(str(each_variant.id)+"_"+"buy_price"):
                buy_price = float(request.POST.get(str(each_variant.id)+"_"+"buy_price"))
                each_variant.buy_price = buy_price

            if request.POST.get(str(each_variant.id)+"_"+"shipment"):
                shipment = int(request.POST.get(str(each_variant.id)+"_"+"shipment"))
                each_variant.shipment = Shipment.objects.get(shipment=shipment)

            if request.POST.get(str(each_variant.id)+"_"+"price"):
                price = int(request.POST.get(str(each_variant.id)+"_"+"price"))
                each_variant.price = price

            if request.POST.get(str(each_variant.id)+"_"+"apply_discount"):
                apply_discount = bool(request.POST.get(str(each_variant.id)+"_"+"apply_discount"))
                # each_variant.apply_discount = apply_discount

            if request.POST.get(str(each_variant.id)+"_"+"discount_percent"):
                discount_percent = int(request.POST.get(str(each_variant.id)+"_"+"discount_percent"))
                each_variant.discount_percent = discount_percent

            if request.POST.get(str(each_variant.id)+"_"+"discount_price"):
                discount_price = int(request.POST.get(str(each_variant.id)+"_"+"discount_price"))
                each_variant.discounted_price = discount_price

            # if request.POST.get(str(each_variant.id)+"_"+"variant"):
            #     variant = request.POST.getlist(str(each_variant.id)+"_"+"variant")

            if request.POST.get(str(each_variant.id)+"_"+"quantity"):
                quantity = request.POST.get(str(each_variant.id)+"_"+"quantity")
                each_variant.num_available = int(quantity)

            if request.POST.get(str(each_variant.id)+"_"+"featured"):
                featured = bool(request.POST.get(str(each_variant.id)+"_"+"featured"))

            if request.POST.get(str(each_variant.id)+"_"+"delivery_time"):
                delivery_time = request.POST.get(str(each_variant.id)+"_"+"delivery_time")
                each_variant.delivery_time = DeliveryTime.objects.get(delivery_time=delivery_time)

            each_variant.save()
        return redirect('shop:admindash')

    #else

    context = {'product':product,
                'variants':variants,
                'categories': Category.objects.all(),
                'image_album':ImageAlbum.objects.all(),
                'all_brands':Brand.objects.all(),
                'attributes':Attribute.objects.all(),
                'delivery_time':DeliveryTime.objects.all(),
                'shipment':Shipment.objects.all()

                }

    return render(request, 'app/product_update.html', context)


@staff_member_required
def remove_variant(request, variant_id):

    ProductVariant.objects.get( pk=variant_id).delete()

    return redirect('shop:admindash')

@staff_member_required
def add_variant(request, product_id):

    product = Product.objects.get(product_id = product_id)
    variants = ProductVariant.objects.filter( variant = product.product_id)

    if request.method == 'POST':

        if request.POST.get("buy_price"):
            buy_price = float(request.POST.get("buy_price"))

        if request.POST.get("shipment"):
            shipment = int(request.POST.get("shipment"))

        if request.POST.get("price"):
            price = int(request.POST.get("price"))

        if request.POST.get("apply_discount"):
            apply_discount = bool(request.POST.get("apply_discount"))

        if request.POST.get("discount_percent"):
            discount_percent = int(request.POST.get("discount_percent"))

        if request.POST.get("discount_price"):
            discount_price = int(request.POST.get("discount_price"))

        if request.POST.get("variant"):
            variant = request.POST.getlist("variant")

        if request.POST.getlist("quantity"):
            quantity = request.POST.getlist("quantity")
            print("Quan: ", quantity)

        if request.POST.get("delivery_time"):
            delivery_time = request.POST.get("delivery_time")

        for i in range(len(variant)):
            print("Variant", variant)
            each_variant=variant[i]
            print("Each Variant",each_variant)
            each_quantity=int(quantity[i])
            ProductVariant.objects.create(
            variant = product,
            attribute = Attribute.objects.get(attribute=each_variant, attribute_category=product.category ),
            delivery_time = DeliveryTime.objects.get(delivery_time=delivery_time),
            buy_price = buy_price,
            shipment= Shipment.objects.get(shipment=shipment),
            price = price,
            apply_discount = apply_discount,
            discount_percent = discount_percent,
            discounted_price = discount_price,
            num_available=each_quantity)

        return redirect('shop:admindash')
    context = {'product':product,
            'variants':variants,
            'categories': Category.objects.all(),
            'image_album':ImageAlbum.objects.all(),
            'all_brands':Brand.objects.all(),
            'shipments':Shipment.objects.all(),
            'attributes':Attribute.objects.filter(attribute_category = product.category),
            'delivery_time':DeliveryTime.objects.all(),

            }

    return render(request, 'app/add_variant.html', context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@staff_member_required
def admin_dashboard(request):

    mega_dict={}

    all_products = Product.objects.all()


    if request.POST.get("variant") and not(request.POST.get("brand")) and not(request.POST.get("category")):
        variant = request.POST.getlist("variant")
        filtered_attributes = Attribute.objects.filter(attribute__in=variant)
        list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
        all_products = Product.objects.filter(product_id__in=list(list_values))

    if request.POST.get("category") and not(request.POST.get("brand")) and not(request.POST.get("variant")):
        categories = request.POST.getlist("category")
        filtered_categories = Category.objects.filter(cat_name__in=categories)
        # all_products = Product.objects.filter(category__in=list(filtered_categories)).values_list('category', flat=True)
        all_products = Product.objects.filter(category__in=list(filtered_categories))

    if request.POST.get("brand") and not(request.POST.get("category")) and not(request.POST.get("variant")):
        brands = request.POST.getlist("brand")
        filtered_brands = Brand.objects.filter(brand_name__in=brands)
        # all_products = Product.objects.filter(category__in=list(filtered_categories)).values_list('category', flat=True)
        all_products = Product.objects.filter(brand__in=list(filtered_brands))

    if request.POST.get("brand") and request.POST.get("category") and not(request.POST.get("variant")):
        categories = request.POST.getlist("category")
        filtered_categories = Category.objects.filter(cat_name__in=categories)
        brands = request.POST.getlist("brand")
        filtered_brands = Brand.objects.filter(brand_name__in=brands)
        # all_products = Product.objects.filter(category__in=list(filtered_categories)).values_list('category', flat=True)
        all_products = Product.objects.filter(category__in=list(filtered_categories),brand__in=list(filtered_brands) )

    if request.POST.get("brand") and request.POST.get("variant") and not(request.POST.get("category")):

        variant = request.POST.getlist("variant")
        filtered_attributes = Attribute.objects.filter(attribute__in=variant)
        list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)

        brands = request.POST.getlist("brand")
        filtered_brands = Brand.objects.filter(brand_name__in=brands)
        all_products = Product.objects.filter(brand__in=list(filtered_brands),product_id__in=list(list_values))

    if request.POST.get("variant") and request.POST.get("category") and not(request.POST.get("brand")):

        variant = request.POST.getlist("variant")
        filtered_attributes = Attribute.objects.filter(attribute__in=variant)
        list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)

        categories = request.POST.getlist("category")
        filtered_categories = Category.objects.filter(cat_name__in=categories)
        all_products = Product.objects.filter(category__in=list(filtered_categories),product_id__in=list(list_values))

    if request.POST.get("variant") and request.POST.get("category") and request.POST.get("brand"):

        variant = request.POST.getlist("variant")
        filtered_attributes = Attribute.objects.filter(attribute__in=variant)
        list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)

        brands = request.POST.getlist("brand")
        filtered_brands = Brand.objects.filter(brand_name__in=brands)

        categories = request.POST.getlist("category")
        filtered_categories = Category.objects.filter(cat_name__in=categories)

        all_products = Product.objects.filter(category__in=list(filtered_categories), brand__in=list(filtered_brands),product_id__in=list(list_values))

    filtered_products = Product.objects.all()

    sizes = []
    for each_product in filtered_products:
        variants = ProductVariant.objects.filter( variant = each_product.product_id)
        for each_variant in variants:
            sizes.append(each_variant.attribute.attribute)

    sizes = set(sizes)

    all_products = all_products.order_by('-updated_at')
    if request.POST.get("sort_by"):

        sortby = request.POST.get("sort_by")
        print("SORTBY", sortby)

        if sortby == 'Price(High to Low)':
            all_products = all_products.order_by('-discounted_price')

        if sortby == 'Price(Low to High)':
            all_products = all_products.order_by('discounted_price')

        if sortby == 'Recently Added':
            all_products = all_products.order_by('-updated_at')

        if sortby == '% OFF':
            all_products = all_products.order_by('discount_percent')


    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        print("Each Product", each_product)
        image_value = getattr(each_product, "image")
        print("Image Value", image_value)
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict

    context = {
        'all_products':Product.objects.all(),
        'product_variants':ProductVariant.objects.all(),
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories':Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text':'All Products',
        'all_brands':Brand.objects.all(),
         'mega_dict': mega_dict,
          'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
          'sizes':sizes,
        'page_obj':all_products,
    }

    return render(request, 'app/admindash.html', context)


def shipment_dashboard(request, id):

    mega_dict={}

    shipment_number = Shipment.objects.filter(shipment=id)
    list_values = ProductVariant.objects.filter(shipment__in=shipment_number).values_list('variant', flat=True)
    all_products = Product.objects.filter(product_id__in=list(list_values))
    all_products = all_products.order_by('-updated_at')

    if request.POST.get("sort_by"):

        sortby = request.POST.get("sort_by")
        print("SORTBY", sortby)

        if sortby == 'Price(High to Low)':
            all_products = all_products.order_by('-discounted_price')

        if sortby == 'Price(Low to High)':
            all_products = all_products.order_by('discounted_price')

        if sortby == 'Recently Added':
            all_products = all_products.order_by('-updated_at')

        if sortby == '% OFF':
            all_products = all_products.order_by('discount_percent')

    p = Paginator(all_products, 30)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}
    all_products = page_obj

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict

    context = {
        'all_products':Product.objects.all(),
        'product_variants':ProductVariant.objects.all(),
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories':Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text':'All Products',
        'all_brands':Brand.objects.all(),
         'mega_dict': mega_dict,
          'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
        'page_obj':all_products,
    }

    return render(request, 'app/admindash.html', context)

def returnitem(request, variant_id):
    print(variant_id)
    print(request.POST)

    if 'return_reason' in request.POST:
        print("Variant Id", int(variant_id))

        variant = ProductVariant.objects.get(id=variant_id)
        variant.num_available = int(variant.num_available) + 1
        variant.save()

        cart_item = Cart_Items.objects.get(product_variant = variant)
        cart_item.returned = True
        cart_item.product_quantity = cart_item.product_quantity - 1
        cart_item.save()

        Returns.objects.create(
            return_item = cart_item,
            return_cost = request.POST.get("return_cost"),
            return_reason = request.POST.get("return_reason")
        )



        update_soldout_product(variant.variant)

        return redirect('shop:solditems')

    else:
        variant = ProductVariant.objects.get(id=variant_id)
        cart_item = Cart_Items.objects.get(product_variant = variant)
        product = Product.objects.filter(product_id = cart_item.product_variant.variant.product_id).first()
        image_value = getattr(product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        context={
            'image':product_image,
            'variant':variant,
            'cart_item':cart_item,
        }


        return render(request, 'app/returnitem.html', context)


@staff_member_required
def solditems(request):
    mega_dict = {}
    all_products = Cart_Items.objects.all()

    p = Paginator(all_products, 15)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj

    for each_product in all_products:
        product_dict = dict.fromkeys(['item', 'product_image'])
        product_dict['item'] = each_product

        product = Product.objects.filter(product_id = each_product.product_variant.variant.product_id).first()
        print("Variant Id", each_product.product_variant.id)

        print("Product", product)
        image_value = getattr(product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        product_dict['product'] = product
        product_dict['variant'] = each_product.product_variant
        mega_dict[each_product.product_variant.id] = product_dict

    context = {
        'all_products':all_products,
        'product_variants':ProductVariant.objects.all(),
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories':Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text':'All Products',
        'all_brands':Brand.objects.all(),
        'items':Cart_Items.objects.all(),
        'mega_dict': mega_dict,
        'page_obj':page_obj,
    }
    return render(request, 'app/solditems.html', context)


def check_carts_scheduler():
    for each_cart in Cart.objects.filter(cart_ordered=False, checkout_status=False):
        print("Running Cart Check")
        print("Each Cart", each_cart)
    # for each_cart in Cart.objects.filter(cart_ordered=False):
        for each_item in Cart_Items.objects.filter(cart=each_cart):
            print("Cart Item", each_item)
            this_time = datetime.now() - each_item.item_hold_time.replace(tzinfo=None)
            total_seconds = this_time.total_seconds()
            minutes = total_seconds/60
            hold_time_query = Constants.objects.filter(constant_name='hold_time').first()
            if minutes >= int(hold_time_query.constant_value):
                variant_for_cart = ProductVariant.objects.get(variant=each_item.product_variant.variant.product_id, attribute = each_item.product_variant.attribute)
                quantity = int(each_item.product_quantity)
                Cart_Items.objects.filter(cart = each_cart, product_variant = each_item.product_variant).delete()
                variant_for_cart.num_available = int(variant_for_cart.num_available) + quantity
                variant_for_cart.save()
            update_soldout_product(each_item.product_variant.variant)


def check_carts(request):
    for each_cart in Cart.objects.filter(cart_ordered=False, checkout_status=False):
        print("Running Cart Scheduler")
    # for each_cart in Cart.objects.filter(cart_ordered=False):
        print("Each Cart", each_cart)
        for each_item in Cart_Items.objects.filter(cart=each_cart):
            this_time = datetime.now() - each_item.item_hold_time.replace(tzinfo=None)
            total_seconds = this_time.total_seconds()
            minutes = total_seconds/60
            hold_time_query = Constants.objects.filter(constant_name='hold_time').first()
            if minutes >= int(hold_time_query.constant_value):
                variant_for_cart = ProductVariant.objects.get(variant=each_item.product_variant.variant.product_id, attribute = each_item.product_variant.attribute)
                quantity = int(each_item.product_quantity)
                Cart_Items.objects.filter(cart = each_cart, product_variant = each_item.product_variant).delete()
                variant_for_cart.num_available = int(variant_for_cart.num_available) + quantity
                variant_for_cart.save()
                return redirect('shop:cart')
            update_soldout_product(each_item.product_variant.variant)
    return redirect('shop:cart')


# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_carts_scheduler, 'interval', seconds=5)
#     scheduler.start()

def update_soldout():
    for each_product in Product.objects.all():
        variant_count=0
        variants = ProductVariant.objects.filter(variant=each_product.product_id)
        for each_variant in variants:
            variant_count = variant_count + int(each_variant.num_available)
            delivery_time = each_variant.delivery_time

        if variant_count == 0 and each_product.availability_type != 'SoldOut':
            each_product.availability_type = 'SoldOut'
            each_product.save()

        if variant_count != 0 and each_product.availability_type == 'SoldOut':
            if str(delivery_time) == '5 to 7 Working Days':
                each_product.availability_type = 'InStock'
                each_product.save()
            else:
                each_product.availability_type = 'PreOrder'
                each_product.save()


def update_soldout_product(each_product):
    variant_count=0
    variants = ProductVariant.objects.filter(variant=each_product.product_id)
    for each_variant in variants:
        variant_count = variant_count + int(each_variant.num_available)
        delivery_time = each_variant.delivery_time

    if variant_count == 0 and each_product.availability_type != 'SoldOut':
        each_product.availability_type = 'SoldOut'
        each_product.save()

    elif variant_count != 0 and each_product.availability_type == 'SoldOut':

        if str(delivery_time) == "5 to 7 Working Days":
            each_product.availability_type = 'InStock'
            each_product.save()
        else:
            each_product.availability_type = 'PreOrder'
            each_product.save()


@login_required
def subscribe(request):
    print("Subscribed")
    subs_query = SubscriptionList.objects.filter(subscribe_user=request.user).first()
    subs_query.subscribe_status = True
    subs_query.save()
    return redirect('shop:checkout_address')


@login_required
def unsubscribe(request):
    print("Unsubscribed")
    subs_query = SubscriptionList.objects.filter(subscribe_user=request.user).first()
    subs_query.subscribe_status = False
    subs_query.save()
    return redirect('shop:checkout_address')


def shipping(request):
    shipping_query = HtmlField.objects.filter(hf_name='shipping').first()

    context = {
        'value': shipping_query.hf_value,
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories':Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text':'All Products',
        'all_brands':Brand.objects.all(),
    }

    return render(request, 'app/shipping.html', context)


def payment_methods(request):

    pm_query = HtmlField.objects.filter(hf_name='payment_methods').first()

    context = {
        'value': pm_query.hf_value ,
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories':Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text':'All Products',
        'all_brands':Brand.objects.all(),
    }

    return render(request, 'app/payment_methods.html', context)


def terms_conditions(request):

    tc_query = HtmlField.objects.filter(hf_name='terms_conditions').first()

    context = {
        'value': tc_query.hf_value,
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories': Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text': 'All Products',
        'all_brands': Brand.objects.all(),
    }

    return render(request, 'app/terms_conditions.html', context)


def aboutus(request):

    aboutus_query = HtmlField.objects.filter(hf_name='aboutus').first()

    context = {
        'value': aboutus_query.hf_value ,
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories':Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text':'All Products',
        'all_brands':Brand.objects.all(),
    }

    return render(request, 'app/aboutus.html', context)


def publish(request, product_id):
    product = Product.objects.get(product_id = product_id)
    product.is_published = True
    product.save()
    return redirect('shop:admindash')


def unpublish(request, product_id):
    product = Product.objects.get(product_id = product_id)
    product.is_published = False
    product.save()
    return redirect('shop:admindash')


def shopHome(request):

    all_products = Product.objects.all()
    all_products = all_products.filter(is_published=True, is_preorder=False)
    all_products = all_products.order_by('-updated_at')
    preorder_products = Product.objects.filter(is_published=True, is_preorder=True)
    preorder_products = preorder_products.order_by('-updated_at')

    mega_dict={}


    for each_product in all_products[:15]:
        product_dict = dict.fromkeys(['product', 'product_image'])
        product_dict['product'] = each_product
        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)
        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    mega_preorder_dict={}
    for each_product in preorder_products[:15]:
        product_dict = dict.fromkeys(['product', 'product_image'])
        product_dict['product'] = each_product
        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)
        product_dict['product_image'] = product_image
        mega_preorder_dict[each_product.product_id] = product_dict

    context = {'banner': Banner.objects.all().first(),
               'all_products': all_products[:15],
               'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'header_text':'All Products',
               'all_brands':Brand.objects.all(),
               'preorder_products':preorder_products[:15],
               'mega_dict':mega_dict,
               'mega_preorder_dict':mega_preorder_dict,

            #   'cosmetics' : cosmetics,
               }

    return render(request, 'app/home.html', context)


def filter_by_cat_and_size(request, category, size):

    cat = Category.objects.get(cat_slug=category)
    cat_query = Category.objects.filter(cat_slug=category)
    size_bucket = SizeBucket.objects.filter(size_name=SizeName.objects.filter(size_slug=size).first(),attribute__attribute_category=cat)
    print("Size Bucket", size_bucket)


    attribute = size_bucket.values_list('attribute', flat=True).order_by('id')
    print("Attributes", attribute)

    if cat_query.first():
        cat_id = Category.objects.filter(cat_slug=category).first()


        list_values = ProductVariant.objects.filter(attribute__in=attribute).values_list('variant', flat=True)
        all_products = Product.objects.filter(product_id__in=list(list_values),category=cat_id.id,is_published=True).order_by('availability_type')


        sizes = None

        if category != "cosmetics":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            sizes = set(sizes)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),category=cat_id.id)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            # print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('-discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('-updated_at','availability_type')


    else:
        all_products = None



    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj
    # all_products = all_products.order_by('?')


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products, 'images': Image.objects.all(),
            'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'header_text':cat_query.first().cat_name,
               'filter_button':False,
               'sizes':sizes,
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'category':Category.objects.filter(cat_slug=category).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_name':SizeName.objects.get(size_slug=size),

               }

    return render(request, 'app/home_searchby.html', context)


def filter_by_cat(request, category):

    cat = Category.objects.get(cat_slug=category)
    # size_names = SizeName.objects.all()
    size_names = SizeBucket.objects.filter(attribute__attribute_category=cat).values('size_name').distinct()
    size_names = SizeName.objects.filter(id__in=size_names)

    cat_query = Category.objects.filter(cat_slug=category)

    if cat_query.first():
        cat_id = Category.objects.filter(cat_slug=category).first()
        all_products = Product.objects.filter(category=cat_id.id, is_published=True, is_preorder=False).order_by('availability_type')


        sizes = None

        if category != "cosmetics":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            sizes = set(sizes)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),category=cat_id.id, is_preorder=False)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('-discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('availability_type','-updated_at')


    else:
        all_products = None



    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products, 'images': Image.objects.all(),
            'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'header_text':cat_query.first().cat_name,
               'filter_button':False,
               'sizes':sizes,
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'category':Category.objects.filter(cat_slug=category).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_names':size_names,

               }

    return render(request, 'app/home_searchby.html', context)


def filter_by_brand_and_size(request, brand, size):

    size_names = SizeBucket.objects.all().values('size_name').distinct()
    size_names = SizeName.objects.filter(id__in=size_names)
    size_bucket = SizeBucket.objects.filter(size_name=SizeName.objects.filter(size_slug=size).first())
    attribute = size_bucket.values_list('attribute', flat=True).order_by('id')

    brand_query = Brand.objects.filter(brand_slug=brand)

    if brand_query.first():
        brand_name = Brand.objects.filter(brand_slug=brand).first()
        all_products = Product.objects.filter(brand=brand_name, is_published=True).order_by('availability_type')


        if brand != "e.l.f":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id, attribute__in=attribute)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),attribute__in=attribute,brand=brand_name.id, is_preorder=False)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('availability_type','-updated_at')


    else:
        all_products = None


    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products,
               #update later to only brand variants
               'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'header_text':brand_query.first().brand_name,
               'all_brands':Brand.objects.all(),
              'sizes':set(sizes),
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'brand':Brand.objects.filter(brand_slug=brand).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_names':size_names,
               }

    return render(request, 'app/home_searchby.html', context)


def filter_by_brand(request, brand):

    size_names = SizeBucket.objects.all().values('size_name').distinct()
    size_names = SizeName.objects.filter(id__in=size_names)

    brand_query = Brand.objects.filter(brand_slug=brand)

    if brand_query.first():
        brand_name = Brand.objects.filter(brand_slug=brand).first()
        all_products = Product.objects.filter(brand=brand_name, is_published=True, is_preorder=False).order_by('availability_type')


        if brand != "e.l.f":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),brand=brand_name.id, is_preorder=False)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('availability_type','-updated_at')




    else:
        all_products = None


    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products,
               #update later to only brand variants
               'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'header_text':brand_query.first().brand_name,
               'all_brands':Brand.objects.all(),
              'sizes':set(sizes),
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'brand':Brand.objects.filter(brand_slug=brand).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_names':size_names,
               }

    return render(request, 'app/home_searchby.html', context)

def filter_by_subcat(request, category, sub_category):

    print(category, sub_category)
    cat_query = Category.objects.filter(cat_slug=category)
    sub_cat_query = Sub_Category.objects.filter(sub_slug=sub_category)

    if cat_query.first():
        cat_id = Category.objects.filter(cat_slug=category).first()
        sub_cat_id = Sub_Category.objects.filter(sub_slug=sub_category).first()
        all_products = Product.objects.filter(category=cat_id.id, sub_category=sub_cat_id.id)

    else:
        all_products = None

    header_text = str(cat_query.first().cat_name) + " - " + str(sub_cat_query.first().sub_cat_name)
    context = {'all_products': all_products, 'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'header_text':header_text}

    return render(request, 'app/home.html', context)

def filter_by_tag(request, tag):
    tag_query = Product.objects.filter(product_tags__name__in=[tag])
    sizes = None

    if tag_query.first():
        # cat_id = Category.objects.filter(cat_slug=category).first()
        all_products = Product.objects.filter(product_tags__name__in=[tag], is_published=True).order_by('availability_type','-updated_at')

        sizes = []
        for each_product in all_products:
            variants = ProductVariant.objects.filter( variant = each_product.product_id)
            for each_variant in variants:
                sizes.append(each_variant.attribute.attribute)

        sizes = set(sizes)

        if request.POST.get("variant"):
            variant = request.POST.getlist("variant")
            filtered_attributes = Attribute.objects.filter(attribute__in=variant)
            list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
            all_products = Product.objects.filter(product_id__in=list(list_values),product_tags__name__in=[tag], is_preorder=False)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('-discount_percent')

    else:
        all_products = None


    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}
    all_products = page_obj

    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products, 'images': Image.objects.all(),
            'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'header_text':"Search Results for " + tag.capitalize().replace("_"," ") + " items",
               'filter_button':False,
               'sizes':sizes,
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                # 'category':Category.objects.filter(cat_slug=category).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               }

    return render(request, 'app/home_searchby.html', context)

@never_cache
def productview(request, id):


    if request.method == "POST":
        if request.POST.get("size"):
            size = request.POST['size']
            print(size)
            product = Product.objects.filter(product_id=id).first()
            variants = ProductVariant.objects.filter( variant = product.product_id)
            image_value = getattr(product, "image")
            product_images = Image.objects.filter(album=image_value)
            attribute = Attribute.objects.filter(attribute=size).first()
            selected_variant = ProductVariant.objects.filter(variant=product.product_id, attribute = attribute)
            attribute_slug = attribute.attribute_slug
            return redirect(f'/productview/{id}/{attribute_slug}/')


    else:
        try:
            product = Product.objects.filter(product_id=id).first()
            variant = ProductVariant.objects.filter( variant = product.product_id).first()
            attribute_slug = variant.attribute.attribute_slug
            return redirect(f'/productview/{id}/{attribute_slug}/')
        except:
            return render(request, 'app/noproduct.html')


import hitcount # import entire package
from hitcount.models import HitCount
from hitcount.views import HitCountDetailView
from django.views import generic
from django.shortcuts import get_object_or_404
from hitcount.utils import get_hitcount_model

# @never_cache
def productview_details(request, id, attribute_slug):

    product = Product.objects.filter(product_id=id).first()
    variants = ProductVariant.objects.filter( variant = product.product_id)
    image_value = getattr(product, "image")
    product_images = Image.objects.filter(album=image_value)
    attribute = Attribute.objects.filter(attribute_slug=attribute_slug, attribute_category=product.category).first()
    selected_variant = ProductVariant.objects.filter(variant=product.product_id,attribute = attribute)
    print("Selected Variant",product.product_id, attribute,  selected_variant)



    product_hit = get_object_or_404(Product, product_id=id)
    context = {}

    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(product_hit)

    hits = hit_count.hits
    context = {}
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = hitcount.views.HitCountMixin.hit_count(request, hit_count)
    count_hit = True

    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    product_hit.product_views = hits
    product_hit.save()



    if request.method == "POST":
        if request.POST.get("addtocart"):
            # if request.user.is_authenticated:
            # add_to_cart(request, id, attribute_slug)
            return add_to_cart(request, id, attribute_slug)

        else:
            context = {'product': product, 'product_images': product_images,
           'variants':variants,
           'selected_variant': selected_variant,
            # 'successful_submit': False,
           'sub_sub_categories': Sub_Sub_Category.objects.all(),
           'sub_categories':Sub_Category.objects.all(),
           'categories': Category.objects.all(),
           'all_brands':Brand.objects.all(),
           'hit_count':hit_count,}

            return render(request, 'app/productview.html', context)

    else:

        context = {'product': product, 'product_images': product_images,
       'variants':variants,
       'selected_variant': selected_variant,
    #   'successful_submit': False,
       'sub_sub_categories': Sub_Sub_Category.objects.all(),
       'sub_categories':Sub_Category.objects.all(),
       'categories': Category.objects.all(),
       'all_brands':Brand.objects.all(),
       'hit_count':hit_count,
        'request.user':request.user,}

        return render(request, 'app/productview.html', context)


# @login_required
@allow_guest_user
def add_to_cart(request, product_id, attribute_slug):

    for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=True):
        each_cart.checkout_status = False
        each_cart.save()

    id = product_id

    product = Product.objects.filter(product_id=id).first()
    variants = ProductVariant.objects.filter( variant = product.product_id)
    image_value = getattr(product, "image")
    product_images = Image.objects.filter(album=image_value)
    attribute = Attribute.objects.filter(attribute_slug=attribute_slug, attribute_category=product.category).first()
    selected_variant = ProductVariant.objects.filter(variant=product.product_id, attribute = attribute)

    print("I'm in add to cart 2")
    variant = request.POST['addtocart']
    print("Variant", variant)
    quantity = request.POST['quantity']
    print("Quantity", quantity)

    product = Product.objects.filter(product_id=id).first()
    print(product, product.category)
    attribute = Attribute.objects.filter(attribute_slug=attribute_slug, attribute_category=product.category).first()
    print("attribute",attribute)
    variant_for_cart = ProductVariant.objects.get( variant=product, attribute = attribute)


    user_cart_query = Cart.objects.filter(author= request.user, cart_ordered = False)

    if user_cart_query.first():
        print("Cart Exists")
        user_cart = Cart.objects.get(author=request.user, cart_ordered = False)
    else:
        print("New Cart Created")
        Cart.objects.create(author=request.user)
        user_cart = Cart.objects.get(author=request.user, cart_ordered = False)

    cart_query = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart)

    if cart_query.first():
        print("Already exists")
        cart_query = Cart_Items.objects.get(cart = user_cart, product_variant = variant_for_cart)
        cart_query.product_quantity = int(cart_query.product_quantity) + int(quantity)  # change field
        cart_query.item_hold_time = timezone.now()
        cart_query.item_price = variant_for_cart.price
        cart_query.item_discount_percent = variant_for_cart.discount_percent
        cart_query.item_discount_price = variant_for_cart.discounted_price
        cart_query.save() # this will update only

    else:
        print("Does not exist")
        Cart_Items.objects.create(cart = user_cart,
                                  product_variant = variant_for_cart,
                                  product_quantity = quantity,
                                  item_hold_time = timezone.now(),
                                  item_price = variant_for_cart.price,
                                  item_discount_price = variant_for_cart.discounted_price,
                                  item_discount_percent = variant_for_cart.discount_percent)

    variant_for_cart.num_available = variant_for_cart.num_available - int(quantity)
    variant_for_cart.save()
    messages.success(request, "Cart updated!")
    submit_flag = True
    selected_variant = ProductVariant.objects.filter(variant=product, attribute = attribute)

    cart_query = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).first()
    if variant_for_cart.apply_discount:
        cart_query.total_amount = int(cart_query.product_quantity) * variant_for_cart.discounted_price
    else:
        cart_query.total_amount = int(cart_query.product_quantity) * variant_for_cart.price
    cart_query.save()
    print(cart_query)

    update_soldout_product(product)

    context = {'product': product,
               'product_images': product_images,
               'variants':variants,
               'selected_variant': selected_variant,
               'successful_submit': submit_flag,
               'add_item':cart_query,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'categories': Category.objects.all()}

    return render(request, 'app/productview.html', context)

# @login_required
@allow_guest_user
def remove_item(request , product_id, attribute):

    product = Product.objects.filter(product_id=product_id).first()
    attribute = Attribute.objects.filter(attribute=attribute, attribute_category=product.category).first()
    variant_for_cart = ProductVariant.objects.get( variant=product, attribute = attribute)

    user_cart = Cart.objects.get(author=request.user, cart_ordered = False)
    cart_query = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart)

    if cart_query.first():
        print("Already exists")
        quantity = int(cart_query.first().product_quantity)
        Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).delete()
        variant_for_cart.num_available = int(variant_for_cart.num_available) + quantity
        variant_for_cart.save()

    user_cart_all = Cart_Items.objects.filter(cart = user_cart)

    update_soldout_product(product)

    context = {'user_cart':user_cart_all,
            'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'categories': Category.objects.all()}

    # return render(request, 'app/cart.html', context)
    return redirect('shop:cart')
    # return redirect('product_detail', product_id=product_id)


# @login_required
@allow_guest_user
def add_quantity(request, product_id, attribute):

    for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=True):
        each_cart.checkout_status = False
        each_cart.save()

    product = Product.objects.filter(product_id=product_id).first()
    attribute = Attribute.objects.filter(attribute=attribute, attribute_category=product.category).first()
    variant_for_cart = ProductVariant.objects.get( variant=product, attribute = attribute)

    user_cart = Cart.objects.get(author=request.user, cart_ordered = False)
    cart_query = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart)

    if cart_query.first():
        cart_query = Cart_Items.objects.get(cart = user_cart, product_variant = variant_for_cart)
        if int(variant_for_cart.num_available) >= 1:
            cart_query.product_quantity = int(cart_query.product_quantity) + 1  # change field
            variant_for_cart.num_available = int(variant_for_cart.num_available) - 1
            print("Num available", variant_for_cart.num_available)
            cart_query.item_hold_time = timezone.now()
            cart_query.save()
            variant_for_cart.save()

        added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).last()
        if variant_for_cart.apply_discount:
            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.discounted_price
        else:
            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
        added_cart.save()

    user_cart_all = Cart_Items.objects.filter(cart = user_cart)

    update_soldout_product(product)

    return redirect('shop:cart')


# @login_required
@allow_guest_user
def minus_quantity(request, product_id, attribute):

    for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=True):
        each_cart.checkout_status = False
        each_cart.save()


    product = Product.objects.filter(product_id=product_id).first()
    attribute = Attribute.objects.filter(attribute=attribute, attribute_category=product.category).first()
    variant_for_cart = ProductVariant.objects.get( variant=product, attribute = attribute)

    user_cart = Cart.objects.get(author=request.user, cart_ordered = False)
    cart_query = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart)

    if cart_query.first():

        cart_query = Cart_Items.objects.get(cart = user_cart, product_variant = variant_for_cart)
        if int(cart_query.product_quantity) >= 1:
            cart_query.product_quantity = int(cart_query.product_quantity) - 1  # change field
            variant_for_cart.num_available = int(variant_for_cart.num_available) + 1
            cart_query.item_hold_time = timezone.now()
            cart_query.save()
            variant_for_cart.save()
        if int(cart_query.product_quantity) < 1:
            Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).delete()

        added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart)

        if added_cart.first():
            added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).last()
            if variant_for_cart.apply_discount:
                added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.discounted_price
            else:
                added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
            added_cart.save()
    update_soldout_product(product)
    return redirect('shop:cart')


# @login_required
@allow_guest_user
def cart(request):

    cart_hold_disclaimer = HtmlField.objects.filter(hf_name='cart_hold_disclaimer').first()
    user_cart = Cart.objects.filter(author=request.user, cart_ordered = False).first()
    # print("Cart", user_cart)
    user_cart_all = Cart_Items.objects.filter(cart = user_cart)
    # print("UserCart_all",user_cart_all)

    order_dict_details={}
    order_dict={}
    if user_cart_all.first():
        for each_item in user_cart_all:
            variant_for_cart = each_item.product_variant
            print(variant_for_cart)

            added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).last()
            added_cart.savings = int(added_cart.product_quantity) * variant_for_cart.savings_item
            added_cart.grand_total_item = int(added_cart.product_quantity) * variant_for_cart.price

            if variant_for_cart.apply_discount:
                added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.discounted_price

            else:
                added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
            added_cart.save()

            image_value = getattr(each_item.product_variant.variant, "image")
            product_image = Image.objects.get(album=image_value, default=True)

            # order_dict[product_image.icon_image] = each_item, product_image.icon_image
            order_dict_details[each_item] = product_image.icon_image


        cart_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('total_amount'))['total_amount__sum']
        cart_savings_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('savings'))['savings__sum']
        cart_grand_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('grand_total_item'))['grand_total_item__sum']

        print("Cart Total", cart_total)
        user_cart.cart_total = cart_total
        user_cart.cart_savings_total = cart_savings_total
        user_cart.grand_total = cart_grand_total
        user_cart.save()


    context = {'cart_hold_disclaimer':cart_hold_disclaimer.hf_value,
                'user_cart':user_cart_all,
               'cart':user_cart,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'order_dict':order_dict_details,}

    return render(request, 'app/cart.html', context)

# @login_required
@allow_guest_user
def checkout_address(request):

    address_query = DeliveryAddress.objects.filter(author=request.user)
    subs_query = SubscriptionList.objects.filter(subscribe_user=request.user)

    email = request.user.email

    if request.method == "POST":
        print("I'm in POST")

        # for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=False):
        #     each_cart.checkout_status = True
        #     each_cart.save()
        if request.POST.get("fullname"):
            fullname = request.POST.get("fullname")
            print(fullname)
        if request.POST.get("mobilenumber"):
            mobilenumber = request.POST.get("mobilenumber")
            print(mobilenumber)
        if request.POST.get("email"):
            email = request.POST.get("email")
        if request.POST.get("province"):
            province = request.POST.get("province")
            print(province)
        if request.POST.get("city"):
            city = request.POST.get("city")
            print(city)
        if request.POST.get("address"):
            address = request.POST.get("address")
            print(address)


        if address_query.first():
            address_query = address_query.first()
            address_query.full_name = fullname
            address_query.mobile_number = mobilenumber
            address_query.province = province
            address_query.city = city
            address_query.address = address
            address_query.email = email

            address_query.save()
            print("Already exists")
            # context ={'address_query':address_query}
            # return render(request, 'app/checkout.html', context)

        else:
            print("Does not exist")
            DeliveryAddress.objects.create(author=request.user, full_name = fullname, mobile_number = mobilenumber, province = province, city = city, address = address, email=email)


        return redirect('shop:cart')

    address_query = DeliveryAddress.objects.filter(author=request.user)

    if address_query.first():

        print("Already exists and I'm not in POST")
        print(address_query)
        address_query.first().email = email
        address_query.first().save()
        context = {'address_query':address_query.first(),
                  'subs_query':subs_query.first(),
                  'sub_sub_categories': Sub_Sub_Category.objects.all(),
                   'sub_categories':Sub_Category.objects.all(),
                    'categories': Category.objects.all(),
                    'all_brands':Brand.objects.all(),}

        return render(request, 'app/checkout.html', context)


    context = {
          'subs_query':subs_query.first(),
          'sub_sub_categories': Sub_Sub_Category.objects.all(),
           'sub_categories':Sub_Category.objects.all(),
           'categories': Category.objects.all(),
        'all_brands':Brand.objects.all(),
    }

    # return redirect('shop:cart')
    return render(request, 'app/checkout.html', context)

def contact_us(request):

    if request.method == "POST":
        print("this")
        if request.POST.get("fullname"):
            fullname = request.POST.get("fullname")
            print(fullname)
        if request.POST.get("mobilenumber"):
            mobilenumber = request.POST.get("mobilenumber")
            print(mobilenumber)
        if request.POST.get("email"):
            email = request.POST.get("email")
            print(email)
        if request.POST.get("subject"):
            subject = request.POST.get("subject")
            print(subject)
        if request.POST.get("textarea"):
            textarea = request.POST.get("textarea")
            print(textarea)

            message1 = str("Sender: " + fullname + "\n")
            message2 = str("Phone Number: " + mobilenumber + "\n")
            message3 = str("Email Address: " + email + "\n")
            message4 = str("Message: " + textarea)
            message = message1 + message2 + message3 + message4

        try:
            print("Email Sent")
            send_mail(subject, message, 'iyraseshop@gmail.com', ['iyraseshop@gmail.com'], fail_silently=False)
        except BadHeaderError:
            print("Bad Error")
            return HttpResponse('Invalid header found.')

        context = { 'message1' : message1,
                    'message2' : message2,
                    'message3' : message3,
                    'message4' : message4,
                    }

        return render(request, 'app/messagesent.html', context)

    if request.user.is_authenticated:

        address_query = DeliveryAddress.objects.filter(author=request.user)

        context ={'address_query':address_query.first(),
                'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
                  'all_brands':Brand.objects.all(),}
        return render(request, 'app/contact_us.html', context)

    else:
        context ={
                # 'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
                'all_brands':Brand.objects.all(),}
        return render(request, 'app/contact_us.html', context)

@login_required
def order_summary(request):

    checkout_disclaimer = HtmlField.objects.filter(hf_name='checkout_disclaimer_text').first()
    address_query = DeliveryAddress.objects.filter(author=request.user)
    if request.user.is_superuser:
        social_address = SocialDeliveryAddress.objects.all()
    else:
        social_address = None
    promo_code_text='NO PROMOCODE APPLIED'
    promo_flag = False

    # if address exists
    if address_query.first():

        # Fetch user cart
        user_cart = Cart.objects.filter(author=request.user, cart_ordered=False).first()
        # Fetch cart items
        user_cart_all = Cart_Items.objects.filter(cart=user_cart)

        # Set all items status as checkout
        for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=False):
            each_cart.checkout_status = True
            each_cart.save()

        # If a promocode request is received



        if request.GET.get('promo_value'):
            print("PROMO CODE APPLIED")

            # get promocode value
            promo_value = request.GET.get('promo_value')

            # Check if similar Promo code object exists
            promo_query = Promo_Code.objects.filter(promo_code=promo_value, promo_status=True)

            # If promocode exists
            if promo_query.first():

                promo_query = Promo_Code.objects.filter(promo_code = promo_value).first()
                print("Promo Value", promo_value, promo_query.promo_type)


                promo_code_text = promo_query.promo_text
                # calculate promo savings for cart
                promotion_savings = user_cart.cart_total * promo_query.promo_percent/100

                if promo_query.promo_type == 'tag_based':

                    if user_cart_all.first():

                        order_dict_details={}
                        # For each item in user cart
                        for each_item in user_cart_all:
                            # Get variant
                            variant_for_cart = each_item.product_variant

                            if variant_for_cart.variant.product_tags.all().first():

                                for each_value in variant_for_cart.variant.product_tags.all():
                                    if each_value.name == promo_query.promo_tag:
                                        added_cart = each_item
                                        # added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).first()
                                        added_cart.savings = int(added_cart.product_quantity) * variant_for_cart.savings_item
                                        added_cart.promo_savings = int(added_cart.product_quantity) * variant_for_cart.discounted_price * promo_query.promo_percent/100
                                        added_cart.grand_total_item = int(added_cart.product_quantity) * variant_for_cart.price

                                        if variant_for_cart.apply_discount:
                                            added_cart.total_amount = (int(added_cart.product_quantity) * variant_for_cart.discounted_price)
                                            added_cart.promo_total_amount = int((int(added_cart.product_quantity) * variant_for_cart.discounted_price) - added_cart.promo_savings)
                                            added_cart.promo_unit_amount = int(added_cart.promo_total_amount / (int(added_cart.product_quantity)))

                                        else:
                                            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
                                        added_cart.save()
                                    else:
                                        added_cart = each_item
                                        added_cart.savings = int(added_cart.product_quantity) * variant_for_cart.savings_item
                                        added_cart.promo_savings = 0
                                        added_cart.grand_total_item = int(added_cart.product_quantity) * variant_for_cart.price

                                        if variant_for_cart.apply_discount:
                                            added_cart.total_amount = (int(added_cart.product_quantity) * variant_for_cart.discounted_price)
                                            added_cart.promo_total_amount = (int(added_cart.product_quantity) * variant_for_cart.discounted_price) - added_cart.promo_savings
                                            added_cart.promo_unit_amount = added_cart.promo_total_amount / (int(added_cart.product_quantity))
                                        else:
                                            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
                                        added_cart.save()

                            else:
                                added_cart = each_item
                                added_cart.savings = int(added_cart.product_quantity) * variant_for_cart.savings_item
                                added_cart.promo_savings = 0
                                added_cart.grand_total_item = int(added_cart.product_quantity) * variant_for_cart.price

                                if variant_for_cart.apply_discount:
                                    added_cart.total_amount = (int(added_cart.product_quantity) * variant_for_cart.discounted_price)
                                    added_cart.promo_total_amount = (int(added_cart.product_quantity) * variant_for_cart.discounted_price) - added_cart.promo_savings
                                    added_cart.promo_unit_amount = added_cart.promo_total_amount / (int(added_cart.product_quantity))
                                else:
                                    added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
                                added_cart.save()
                            image_value = getattr(each_item.product_variant.variant, "image")
                            product_image = Image.objects.get(album=image_value, default=True)
                            order_dict_details[each_item] = product_image.icon_image


                        cart_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('total_amount'))['total_amount__sum']
                        cart_savings_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('savings'))['savings__sum']
                        cart_savings_promo = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('promo_savings'))['promo_savings__sum']
                        cart_grand_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('grand_total_item'))['grand_total_item__sum']
                        cart_promo_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('promo_total_amount'))['promo_total_amount__sum']

                        user_cart.cart_promo_savings = cart_savings_promo
                        user_cart.cart_total = cart_total
                        user_cart.cart_savings_total = cart_savings_total
                        user_cart.grand_total = cart_grand_total
                        user_cart.promo_cart_total = cart_promo_total

                        if user_cart.promo_cart_total > 2999:
                            user_cart.delivery_charges = 0
                            user_cart.promo_cart_total = user_cart.promo_cart_total + user_cart.delivery_charges
                        else:
                            user_cart.delivery_charges = 250
                            user_cart.promo_cart_total = user_cart.promo_cart_total + user_cart.delivery_charges

                        user_cart.cart_total = user_cart.promo_cart_total
                        promo_flag = True
                        user_cart.cart_promo_flag = promo_flag
                        user_cart.save()


                    context = {'address_query': address_query.first(),
                       'user_cart':user_cart_all,
                       'cart':user_cart,
                   'sub_sub_categories': Sub_Sub_Category.objects.all(),
                   'sub_categories':Sub_Category.objects.all(),
                   'categories': Category.objects.all(),
                   'all_brands':Brand.objects.all(),
                   'checkout_disclaimer':checkout_disclaimer.hf_value,
                    'promo_code_text':promo_code_text,
                    'promo_flag':promo_flag,
                    'social_address':social_address,
                    'order_dict':order_dict_details,
                   }

                    return render(request, 'app/order_summary.html', context)

                else:

                    # If user cart exists
                    if user_cart_all.first():
                        order_dict_details={}
                        # For each item in user cart
                        for each_item in user_cart_all:



                            # Get variant
                            variant_for_cart = each_item.product_variant
                            added_cart = each_item
                            # added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).first()
                            added_cart.savings = int(added_cart.product_quantity) * variant_for_cart.savings_item
                            added_cart.promo_savings = int(added_cart.product_quantity) * variant_for_cart.discounted_price * promo_query.promo_percent/100
                            added_cart.grand_total_item = int(added_cart.product_quantity) * variant_for_cart.price

                            print("Promo Savings", added_cart.promo_savings)
                            if variant_for_cart.apply_discount:
                                added_cart.total_amount = (int(added_cart.product_quantity) * variant_for_cart.discounted_price)
                                added_cart.promo_total_amount = int((int(added_cart.product_quantity) * variant_for_cart.discounted_price) - added_cart.promo_savings)
                                added_cart.promo_unit_amount = int(added_cart.promo_total_amount / (int(added_cart.product_quantity)))
                            else:
                                added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
                            added_cart.save()
                            image_value = getattr(each_item.product_variant.variant, "image")
                            product_image = Image.objects.get(album=image_value, default=True)
                            order_dict_details[each_item] = product_image.icon_image

                        cart_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('total_amount'))['total_amount__sum']
                        cart_savings_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('savings'))['savings__sum']
                        cart_savings_promo = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('promo_savings'))['promo_savings__sum']
                        cart_grand_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('grand_total_item'))['grand_total_item__sum']
                        cart_promo_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('promo_total_amount'))['promo_total_amount__sum']

                        user_cart.cart_promo_savings = cart_savings_promo
                        user_cart.cart_total = cart_total
                        user_cart.cart_savings_total = cart_savings_total
                        user_cart.grand_total = cart_grand_total
                        user_cart.promo_cart_total = cart_promo_total

                        if user_cart.promo_cart_total > 2999:
                            user_cart.delivery_charges = 0
                            user_cart.promo_cart_total = user_cart.promo_cart_total + user_cart.delivery_charges
                        else:
                            user_cart.delivery_charges = 250
                            user_cart.promo_cart_total = user_cart.promo_cart_total + user_cart.delivery_charges


                        user_cart.cart_total = user_cart.promo_cart_total
                        promo_flag = True
                        user_cart.cart_promo_flag = promo_flag
                        user_cart.save()


                    context = {'address_query': address_query.first(),
                       'user_cart':user_cart_all,
                       'cart':user_cart,
                   'sub_sub_categories': Sub_Sub_Category.objects.all(),
                   'sub_categories':Sub_Category.objects.all(),
                   'categories': Category.objects.all(),
                   'all_brands':Brand.objects.all(),
                   'checkout_disclaimer':checkout_disclaimer.hf_value,
                    'promo_code_text':promo_code_text,
                    'promo_flag':promo_flag,
                    'social_address':social_address,
                   'order_dict':order_dict_details,


                   }

                    return render(request, 'app/order_summary.html', context)

            else:

                promo_code_text = promo_value + ' - INVALID PROMOCODE'

                if user_cart_all.first():
                    order_dict_details={}
                    for each_item in user_cart_all:
                        variant_for_cart = each_item.product_variant

                        added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).last()
                        added_cart.savings = int(added_cart.product_quantity) * variant_for_cart.savings_item
                        added_cart.grand_total_item = int(added_cart.product_quantity) * variant_for_cart.price

                        if variant_for_cart.apply_discount:
                            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.discounted_price

                        else:
                            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
                        image_value = getattr(each_item.product_variant.variant, "image")
                        product_image = Image.objects.get(album=image_value, default=True)
                        order_dict_details[each_item] = product_image.icon_image
                    cart_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('total_amount'))['total_amount__sum']
                    cart_savings_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('savings'))['savings__sum']
                    cart_grand_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('grand_total_item'))['grand_total_item__sum']

                    promo_flag = False




                    user_cart.cart_total = cart_total
                    user_cart.cart_savings_total = cart_savings_total
                    user_cart.grand_total = cart_grand_total
                    user_cart.cart_promo_flag = promo_flag
                    user_cart.cart_total = cart_total

                    if user_cart.cart_total > 2999:
                        user_cart.delivery_charges = 0
                        user_cart.cart_total = user_cart.cart_total + user_cart.delivery_charges
                    else:
                        user_cart.delivery_charges = 250
                        user_cart.cart_total = user_cart.cart_total + user_cart.delivery_charges

                    user_cart.save()


        else:
            print("PROMO CODE NOT APPLIED")
            if user_cart_all.first():
                order_dict_details={}
                for each_item in user_cart_all:
                    variant_for_cart = each_item.product_variant

                    added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).last()
                    added_cart.savings = int(added_cart.product_quantity) * variant_for_cart.savings_item
                    added_cart.grand_total_item = int(added_cart.product_quantity) * variant_for_cart.price

                    if variant_for_cart.apply_discount:
                        added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.discounted_price

                    else:
                        added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
                    added_cart.save()
                    image_value = getattr(each_item.product_variant.variant, "image")
                    product_image = Image.objects.get(album=image_value, default=True)
                    order_dict_details[each_item] = product_image.icon_image

                cart_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('total_amount'))['total_amount__sum']
                cart_savings_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('savings'))['savings__sum']
                cart_grand_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('grand_total_item'))['grand_total_item__sum']

                user_cart.cart_total = cart_total
                user_cart.cart_savings_total = cart_savings_total
                user_cart.grand_total = cart_grand_total
                user_cart.cart_promo_flag = promo_flag
                user_cart.cart_total = cart_total

                if user_cart.cart_total > 2999:
                    user_cart.delivery_charges = 0
                    user_cart.cart_total = user_cart.cart_total + user_cart.delivery_charges
                else:
                    user_cart.delivery_charges = 250
                    user_cart.cart_total = user_cart.cart_total + user_cart.delivery_charges

                user_cart.save()


        context = {'address_query': address_query.first(),
                   'user_cart':user_cart_all,
                   'cart':user_cart,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'checkout_disclaimer':checkout_disclaimer.hf_value,
                'promo_code_text':promo_code_text,
                'promo_flag':promo_flag,
                'social_address':social_address,
                'order_dict':order_dict_details,


               }

        return render(request, 'app/order_summary.html', context)

    # if address doesn't exists -> Go to Address fill
    else:
        # But first, mark everything as checkout
        for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=False):
            each_cart.checkout_status = True
            each_cart.save()

        return render(request, 'app/checkout.html')

    return render(request, 'app/checkout.html')

@allow_guest_user
@never_cache
def placeorder(request):
    # update cart Item times

    user_cart = Cart.objects.filter(author=request.user,cart_ordered = False)
    user_address = DeliveryAddress.objects.get(author=request.user)
    address_query = DeliveryAddress.objects.filter(author=request.user)
    print("Request User", request.user)
    print("DeliveryAddress", address_query)
    print("USer Address", user_address)

    if user_cart.first():
        user_cart = Cart.objects.filter(author=request.user,cart_ordered = False).first()

        if Cart_Items.objects.filter(cart = user_cart).first():

            order = UserOrder.objects.create(author = request.user, order_cart = user_cart, order_address = user_address)
            user_cart.cart_ordered = True
            user_cart_all = Cart_Items.objects.filter(cart=user_cart)
            user_cart.save()

        else:
            # return HttpResponse('Your cart is empty')
            return redirect('shop:cart')

        logo = Logo.objects.filter(logo_text='logo').first()

        if user_address.email:
            email = user_address.email
        else:
            email = request.user.email



        ctx = {
            'site':'https://www.iyraseshop.com',
            'username': request.user.username,
            'email': email,
            'logo':logo.logo_image,
            'user_cart': user_cart_all,
            'cart': user_cart,
            'address':address_query.first(),
            'user':request.user,
            }


        message = get_template('app/order_placed_email.html').render(ctx)

        print("Email", email)
        send_mail(
            "Thank you for placing your order with Iyra's Eshop",
            message,
            'iyraseshop@gmail.com',
            [email, 'iyraseshop@gmail.com',],
            fail_silently=False,
            html_message=message,)


        context = {'user_cart': user_cart_all,
                   'cart': user_cart,
                   'order': order.order_id,
                   'sub_sub_categories': Sub_Sub_Category.objects.all(),
                   'sub_categories':Sub_Category.objects.all(),
                   'categories': Category.objects.all(),
                   'all_brands':Brand.objects.all(),}
        return render(request, 'app/placeorder.html', context)

    else:
        # return HttpResponse('Nothing to order')
        return redirect('shop:cart')

@login_required
def myorders(request):

    user_orders = UserOrder.objects.filter(author=request.user)
    user_cart = Cart.objects.filter(author=request.user)

    cart_items =[]
    for each_value in user_cart:
        cart_items.append(each_value.id)

    order_dict_all = {}
    for each_order in user_orders:
        order_dict = {}
        order_dict = dict.fromkeys(['order', 'author','cart','items'])
        order_dict['order'] = each_order
        order_dict['author'] = each_order.author
        order_dict['cart'] = each_order.order_cart
        # user_cart_items = Cart_Items.objects.filter(cart__id__in=cart_items)
        order_dict['items'] = Cart_Items.objects.filter(cart=each_order.order_cart)
        user_cart_all = Cart_Items.objects.filter(cart=each_order.order_cart)
        order_dict_details = {}
        for each_item in order_dict['items']:
            image_value = getattr(each_item.product_variant.variant, "image")
            product_image = Image.objects.get(album=image_value, default=True)
            order_dict_details[product_image.icon_image] = each_item
        order_dict['items_list'] = order_dict_details
        order_dict_all[each_order.order_id] = order_dict

    context = {'user_orders': user_orders,
               'user_cart': user_cart,
               'user_cart_all': user_cart_all,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories': Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'myorders': order_dict_all,
               }

    return render(request, 'app/myorders.html', context)

@staff_member_required
def allorders(request):


    allorders = UserOrder.objects.all()
    user_orders = UserOrder.objects.all()
    user_cart = Cart.objects.all()


    order_dict_all={}
    allorders = allorders.order_by('-order_id')

    p = Paginator(allorders, 15)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}
    allorders = page_obj

    for each_order in allorders:
        order_dict = {}
        order_dict = dict.fromkeys(['order', 'author','cart','items'])
        order_dict['order'] = each_order
        order_dict['author'] = each_order.author
        order_dict['cart'] = each_order.order_cart
        # user_cart_items = Cart_Items.objects.filter(cart__id__in=cart_items)
        order_dict['items'] = Cart_Items.objects.filter(cart=each_order.order_cart)
        user_cart_all = Cart_Items.objects.filter(cart=each_order.order_cart)
        order_dict_details = {}
        for each_item in order_dict['items']:
            print("Each Item", each_item, each_item.product_variant.variant)
            image_value = getattr(each_item.product_variant.variant, "image")
            product_image = Image.objects.get(album=image_value, default=True)
            order_dict_details[product_image.icon_image, each_item.product_variant.attribute] = each_item
        order_dict['items_list'] = order_dict_details
        order_dict_all[each_order.order_id] = order_dict


    context = {'all_orders':allorders,
                'user_orders': user_orders,
               'user_cart': user_cart,
               'user_cart_all': user_cart_all,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories': Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'order_dict':order_dict,
               'order_dict_all':order_dict_all,
               'page_obj':page_obj,}

    return render(request, 'app/allorders.html', context)

@staff_member_required
def summary(request):
    payment_periods = TCSPaymentPeriod.objects.values('payment_period')
    records = TCSPaymentPeriod.objects.filter(payment_period__in=[item['payment_period'] for item in payment_periods])

    user_orders = UserOrder.objects.all()
    user_cart = Cart.objects.all()

    tcs_record = {}
    for each_record in records:
        allorders = UserOrder.objects.filter(tcsorder=each_record)
        order_dict_all={}
        for each_order in allorders:
            order_dict = {}
            order_dict = dict.fromkeys(['order', 'author','cart','items'])
            order_dict['order'] = each_order
            order_dict['author'] = each_order.author
            order_dict['cart'] = each_order.order_cart
            # user_cart_items = Cart_Items.objects.filter(cart__id__in=cart_items)
            order_dict['items'] = Cart_Items.objects.filter(cart=each_order.order_cart)
            user_cart_all = Cart_Items.objects.filter(cart=each_order.order_cart)
            order_dict_details = {}
            for each_item in order_dict['items']:
                image_value = getattr(each_item.product_variant.variant, "image")
                product_image = Image.objects.get(album=image_value, default=True)
                order_dict_details[product_image.icon_image] = each_item
            order_dict['items_list'] = order_dict_details
            order_dict_all[each_order.order_id] = order_dict
        tcs_record[each_record.payment_period] = order_dict_all


    context = {'all_orders':allorders,
                'user_orders': user_orders,
               'user_cart': user_cart,
               'user_cart_all': user_cart_all,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories': Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'order_dict':order_dict,
               'order_dict_all':order_dict_all,
               'tcs_record':tcs_record}

    return render(request, 'app/summary.html', context)

def preorder(request):

    all_products = Product.objects.filter(is_published=True,is_preorder=True)
    all_products = all_products.order_by('-updated_at')

    brands_list = all_products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)


    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products,
               #update later to only brand variants
               'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               # 'header_text':brand_query.first().brand_name,
               'all_brands':all_brands,
              # 'sizes':set(sizes),
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                # 'brand':Brand.objects.filter(brand_slug=brand).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               # 'size_names':size_names,
               }

    # context = {'banner': Banner.objects.all().first(),
    #            'all_products': all_products[:15],
    #            'images': Image.objects.all(),
    #            'sub_sub_categories': Sub_Sub_Category.objects.all(),
    #            'sub_categories':Sub_Category.objects.all(),
    #            'categories': Category.objects.all(),
    #            'header_text':'All Products',
    #            'all_brands':Brand.objects.all(),
    #            }

    return render(request, 'app/preorderportal.html', context)

def filter_by_cat_and_size_preorder(request, category, size):

    cat = Category.objects.get(cat_slug=category)
    cat_query = Category.objects.filter(cat_slug=category)
    size_bucket = SizeBucket.objects.filter(size_name=SizeName.objects.filter(size_slug=size).first(),attribute__attribute_category=cat)
    print("Size Bucket", size_bucket)


    attribute = size_bucket.values_list('attribute', flat=True).order_by('id')
    print("Attributes", attribute)

    if cat_query.first():
        cat_id = Category.objects.filter(cat_slug=category).first()


        list_values = ProductVariant.objects.filter(attribute__in=attribute).values_list('variant', flat=True)
        all_products = Product.objects.filter(product_id__in=list(list_values),category=cat_id.id,is_published=True, is_preorder=True).order_by('-updated_at')

        sizes = None

        if category != "cosmetics":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            sizes = set(sizes)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),category=cat_id.id, is_preorder=True)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            # print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('-discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('availability_type','-updated_at')

    else:
        all_products = None

    products = Product.objects.filter(is_published=True, is_preorder=True)
    brands_list = products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)

    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj
    # all_products = all_products.order_by('?')


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products, 'images': Image.objects.all(),
            'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':all_brands,
               'header_text':cat_query.first().cat_name,
               'filter_button':False,
               'sizes':sizes,
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'category':Category.objects.filter(cat_slug=category).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_name':SizeName.objects.get(size_slug=size),

               }

    return render(request, 'app/home_searchby_preorder.html', context)

def filter_by_cat_preorder(request, category):

    cat = Category.objects.get(cat_slug=category)
    # size_names = SizeName.objects.all()
    size_names = SizeBucket.objects.filter(attribute__attribute_category=cat).values('size_name').distinct()
    size_names = SizeName.objects.filter(id__in=size_names)

    cat_query = Category.objects.filter(cat_slug=category)

    if cat_query.first():
        cat_id = Category.objects.filter(cat_slug=category).first()
        all_products = Product.objects.filter(category=cat_id.id, is_published=True, is_preorder=True).order_by('-updated_at')


        sizes = None

        if category != "cosmetics":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            sizes = set(sizes)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),category=cat_id.id, is_preorder=True)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('-discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('availability_type','-updated_at')
    else:
        all_products = None


    products = Product.objects.filter(is_published=True, is_preorder=True)
    brands_list = products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)

    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products, 'images': Image.objects.all(),
            'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':all_brands,
               'header_text':cat_query.first().cat_name,
               'filter_button':False,
               'sizes':sizes,
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'category':Category.objects.filter(cat_slug=category).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_names':size_names,

               }

    return render(request, 'app/home_searchby_preorder.html', context)

def filter_by_brand_and_size_preorder(request, brand, size):

    size_names = SizeBucket.objects.all().values('size_name').distinct()
    size_names = SizeName.objects.filter(id__in=size_names)
    size_bucket = SizeBucket.objects.filter(size_name=SizeName.objects.filter(size_slug=size).first())
    attribute = size_bucket.values_list('attribute', flat=True).order_by('id')

    brand_query = Brand.objects.filter(brand_slug=brand)

    if brand_query.first():
        brand_name = Brand.objects.filter(brand_slug=brand).first()
        all_products = Product.objects.filter(brand=brand_name, is_published=True, is_preorder=True).order_by('-updated_at')

        if brand != "e.l.f":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id, attribute__in=attribute)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),attribute__in=attribute,brand=brand_name.id, is_preorder=True)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('availability_type','-updated_at')

    else:
        all_products = None

    products = Product.objects.filter(is_published=True, is_preorder=True)
    brands_list = products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)

    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products,
               #update later to only brand variants
               'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'header_text':brand_query.first().brand_name,
               'all_brands':all_brands,
              'sizes':set(sizes),
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'brand':Brand.objects.filter(brand_slug=brand).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_names':size_names,
               }

    return render(request, 'app/home_searchby_preorder.html', context)

def filter_by_brand_preorder(request, brand):

    size_names = SizeBucket.objects.all().values('size_name').distinct()
    size_names = SizeName.objects.filter(id__in=size_names)

    brand_query = Brand.objects.filter(brand_slug=brand)

    if brand_query.first():
        brand_name = Brand.objects.filter(brand_slug=brand).first()
        all_products = Product.objects.filter(brand=brand_name, is_published=True, is_preorder=True).order_by('-updated_at')

        if brand != "e.l.f":
            sizes = []
            for each_product in all_products:
                variants = ProductVariant.objects.filter( variant = each_product.product_id)
                for each_variant in variants:
                    sizes.append(each_variant.attribute.attribute)

            if request.POST.get("variant"):
                variant = request.POST.getlist("variant")
                filtered_attributes = Attribute.objects.filter(attribute__in=variant)
                list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
                all_products = Product.objects.filter(product_id__in=list(list_values),brand=brand_name.id, is_preorder=True)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('discount_percent')
        else:
            # all_products = all_products.order_by('availability_type')
            all_products = all_products.order_by('availability_type','-updated_at')



    else:
        all_products = None

    products = Product.objects.filter(is_published=True, is_preorder=True)
    brands_list = products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)

    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products,
               #update later to only brand variants
               'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'header_text':brand_query.first().brand_name,
               'all_brands':all_brands,
              'sizes':set(sizes),
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                'brand':Brand.objects.filter(brand_slug=brand).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               'size_names':size_names,
               }

    return render(request, 'app/home_searchby_preorder.html', context)

def filter_by_subcat_preorder(request, category, sub_category):

    print(category, sub_category)
    cat_query = Category.objects.filter(cat_slug=category)
    sub_cat_query = Sub_Category.objects.filter(sub_slug=sub_category)

    if cat_query.first():
        cat_id = Category.objects.filter(cat_slug=category).first()
        sub_cat_id = Sub_Category.objects.filter(sub_slug=sub_category).first()
        all_products = Product.objects.filter(category=cat_id.id, sub_category=sub_cat_id.id, is_preorder=True)

    else:
        all_products = None

    products = Product.objects.filter(is_published=True, is_preorder=True)
    brands_list = products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)

    header_text = str(cat_query.first().cat_name) + " - " + str(sub_cat_query.first().sub_cat_name)
    context = {'all_products': all_products, 'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':all_brands,
               'header_text':header_text}

    return render(request, 'app/home.html', context)

def filter_by_tag_preorder(request, tag):
    tag_query = Product.objects.filter(product_tags__name__in=[tag])
    sizes = None

    if tag_query.first():
        # cat_id = Category.objects.filter(cat_slug=category).first()
        all_products = Product.objects.filter(product_tags__name__in=[tag], is_published=True, is_preorder=True).order_by('availability_type','-updated_at')

        sizes = []
        for each_product in all_products:
            variants = ProductVariant.objects.filter( variant = each_product.product_id)
            for each_variant in variants:
                sizes.append(each_variant.attribute.attribute)

        sizes = set(sizes)

        if request.POST.get("variant"):
            variant = request.POST.getlist("variant")
            filtered_attributes = Attribute.objects.filter(attribute__in=variant)
            list_values = ProductVariant.objects.filter(attribute__in=list(filtered_attributes)).values_list('variant', flat=True)
            all_products = Product.objects.filter(product_id__in=list(list_values),product_tags__name__in=[tag], is_preorder=True)

        if request.POST.get("sort_by"):
            sortby = request.POST.get("sort_by")
            print("SORTBY", sortby)

            if sortby == 'Price(High to Low)':
                all_products = all_products.order_by('-discounted_price')

            if sortby == 'Price(Low to High)':
                all_products = all_products.order_by('discounted_price')

            if sortby == 'Recently Added':
                all_products = all_products.order_by('-updated_at')

            if sortby == '% OFF':
                all_products = all_products.order_by('-discount_percent')

    else:
        all_products = None

    products = Product.objects.filter(is_published=True, is_preorder=True)
    brands_list = products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)

    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}
    all_products = page_obj

    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products, 'images': Image.objects.all(),
            'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':all_brands,
               'header_text':"Search Results for " + tag.capitalize().replace("_"," ") + " items",
               'filter_button':False,
               'sizes':sizes,
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
                # 'category':Category.objects.filter(cat_slug=category).first(),
               'page_obj':all_products,
               'mega_dict':mega_dict,
               }

    return render(request, 'app/home_searchby_preorder.html', context)

def shop_all_preorder(request):

    all_products = Product.objects.filter(is_published=True, is_preorder=True).order_by('-updated_at')

    products = Product.objects.filter(is_published=True, is_preorder=True)
    brands_list = products.values_list('brand', flat=True)
    all_brands = Brand.objects.filter(id__in=brands_list)

    if request.POST.get("sort_by"):
        sortby = request.POST.get("sort_by")
        print("SORTBY", sortby)

        if sortby == 'Price(High to Low)':
            all_products = all_products.order_by('-discounted_price')

        if sortby == 'Price(Low to High)':
            all_products = all_products.order_by('discounted_price')

        if sortby == 'Recently Added':
            all_products = all_products.order_by('-updated_at')

        if sortby == '% OFF':
            all_products = all_products.order_by('discount_percent')
    else:
        # all_products = all_products.order_by('availability_type')
        all_products = all_products.order_by('availability_type','-updated_at')


    p = Paginator(all_products, 40)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # context = {'page_obj': page_obj}

    all_products = page_obj


    mega_dict={}

    for each_product in all_products:
        product_dict = dict.fromkeys(['product', 'variants', 'product_image'])
        product_dict['product'] = each_product

        variants = ProductVariant.objects.filter( variant = each_product.product_id)

        product_variants=[]
        for each_variant in variants:
            product_variants.append(each_variant)

        product_dict['variants']=product_variants

        image_value = getattr(each_product, "image")
        product_image = Image.objects.get(album=image_value, default=True)

        product_dict['product_image'] = product_image
        mega_dict[each_product.product_id] = product_dict


    context = {'all_products': all_products,
               #update later to only brand variants
               'all_variants':ProductVariant.objects.all(),
              'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':all_brands,
                'sortby_options':['Choose option','Price(High to Low)','Price(Low to High)','Recently Added','% OFF'],
               'page_obj':all_products,
               'mega_dict':mega_dict,
               }

    return render(request, 'app/home_searchby_preorder.html', context)



# def test_elements():
#     all_variants = ProductVariant.objects.all()
#     for each_variant in all_variants:
#         if each_variant.variant.category == each_variant.attribute.attribute_category:
#             pass
#         else:
#             print("Different",each_variant,each_variant.variant.category,each_variant.attribute.attribute_category)
#             att = Attribute.objects.filter(attribute=each_variant.attribute, attribute_category=each_variant.variant.category)
#             if att.first():
#                 print("Attribute", att)
#                 each_variant.attribute = att.first()
#                 each_variant.save()
#             else:
#                 print("First not found")
#
# test_elements()

#
# def save_cart_prices():
#     print("Saving Cart Prices")
#     cart_query = Cart_Items.objects.all()
#     for each_item in cart_query:
#         variant_for_cart = each_item.product_variant
#         each_item.item_price = variant_for_cart.price
#         each_item.item_discount_percent = variant_for_cart.discount_percent
#         each_item.item_discount_price = variant_for_cart.discounted_price
#         each_item.save()
#
# save_cart_prices()
