from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from shop.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.db.models import Sum
from django.core.mail import send_mail, BadHeaderError
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta


def check_carts_scheduler():
    for each_cart in Cart.objects.filter(cart_ordered=False, checkout_status=False):
    # for each_cart in Cart.objects.filter(cart_ordered=False):
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


def check_carts(request):
    for each_cart in Cart.objects.filter(cart_ordered=False, checkout_status=False):
    # for each_cart in Cart.objects.filter(cart_ordered=False):
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
    return redirect('shop:cart')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_carts_scheduler, 'interval', seconds=300)
    scheduler.start()

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
        'value': shipping_query.my_field,
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

    aboutus_query = HtmlField.objects.filter(hf_name='payment_methods').first()

    context = {
        'value': aboutus_query.hf_value ,
        'sub_sub_categories': Sub_Sub_Category.objects.all(),
        'sub_categories':Sub_Category.objects.all(),
        'categories': Category.objects.all(),
        'header_text':'All Products',
        'all_brands':Brand.objects.all(),
    }

    return render(request, 'app/aboutus.html', context)


def shopHome(request):

    context = {'banner': Banner.objects.all().first(),
               'all_products': Product.objects.all(), 'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'header_text':'All Products',
               'all_brands':Brand.objects.all(),}

    return render(request, 'app/home.html', context)


def filter_by_cat(request, category):

    cat_query = Category.objects.filter(cat_slug=category)

    if cat_query.first():
        cat_id = Category.objects.filter(cat_slug=category).first()
        all_products = Product.objects.filter(category=cat_id.id)

    else:
        all_products = None

    context = {'all_products': all_products, 'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'header_text':cat_query.first().cat_name}

    return render(request, 'app/home_searchby.html', context)


def filter_by_brand(request, brand):

    brand_query = Brand.objects.filter(brand_slug=brand)

    if brand_query.first():
        brand_name = Brand.objects.filter(brand_slug=brand).first()
        all_products = Product.objects.filter(brand=brand_name)

    else:
        all_products = None

    context = {'all_products': all_products, 'images': Image.objects.all(),
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'header_text':brand_query.first().brand_name,
               'all_brands':Brand.objects.all(),}

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

        else:
            product = Product.objects.filter(product_id=id).first()
            variants = ProductVariant.objects.filter( variant = product.product_id)
            image_value = getattr(product, "image")
            product_images = Image.objects.filter(album=image_value)
            selected_variant = ""

    else:
        product = Product.objects.filter(product_id=id).first()
        variants = ProductVariant.objects.filter( variant = product.product_id)
        image_value = getattr(product, "image")
        product_images = Image.objects.filter(album=image_value)
        selected_variant = ""

    context = {'product': product, 'product_images': product_images,
               'variants':variants, 'selected_variant': selected_variant,
               'successful_submit': False,
                'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),}

    return render(request, 'app/productview.html', context)



@login_required
def add_to_cart(request, product_id, attribute):

    id = product_id
    cart_query = None

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
            submit_flag = False

        else:
            product = Product.objects.filter(product_id=id).first()
            variants = ProductVariant.objects.filter( variant = product.product_id)
            image_value = getattr(product, "image")
            product_images = Image.objects.filter(album=image_value)
            selected_variant = ""
            submit_flag = False

    else:
        product = Product.objects.filter(product_id=id).first()
        variants = ProductVariant.objects.filter( variant = product.product_id)
        image_value = getattr(product, "image")
        product_images = Image.objects.filter(album=image_value)
        selected_variant = ""
        submit_flag = False
        cart_query = None

    if request.method == "POST":
        print("Product_ID", product_id)
        print("attribute", attribute)
        print("I'm in add to cart")

        if request.POST.get("addtocart"):
            print("I'm in add to cart 2")
            variant = request.POST['addtocart']
            print("Variant", variant)
            quantity = request.POST['quantity']
            print("Quantity", quantity)

            product = Product.objects.filter(product_id=product_id).first()
            attribute = Attribute.objects.filter(attribute=attribute).first()
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
                cart_query.item_hold_time = datetime.now()
                cart_query.save() # this will update only

            else:
                print("Does not exist")
                Cart_Items.objects.create(cart = user_cart, product_variant = variant_for_cart, product_quantity = quantity, item_hold_time = datetime.now())

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


@login_required
def remove_item(request , product_id, attribute):

    product = Product.objects.filter(product_id=product_id).first()
    attribute = Attribute.objects.filter(attribute=attribute).first()
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

    context = {'user_cart':user_cart_all,
            'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'categories': Category.objects.all()}

    # return render(request, 'app/cart.html', context)
    return redirect('shop:cart')
    # return redirect('product_detail', product_id=product_id)


@login_required
def add_quantity(request, product_id, attribute):

    for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=True):
        each_cart.checkout_status = False
        each_cart.save()

    product = Product.objects.filter(product_id=product_id).first()
    attribute = Attribute.objects.filter(attribute=attribute).first()
    variant_for_cart = ProductVariant.objects.get( variant=product, attribute = attribute)

    user_cart = Cart.objects.get(author=request.user, cart_ordered = False)
    cart_query = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart)

    if cart_query.first():
        cart_query = Cart_Items.objects.get(cart = user_cart, product_variant = variant_for_cart)
        if int(variant_for_cart.num_available) >= 1:
            cart_query.product_quantity = int(cart_query.product_quantity) + 1  # change field
            variant_for_cart.num_available = int(variant_for_cart.num_available) - 1
            print("Num available", variant_for_cart.num_available)
            cart_query.item_hold_time = datetime.now()
            cart_query.save()
            variant_for_cart.save()

        added_cart = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart).last()
        if variant_for_cart.apply_discount:
            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.discounted_price
        else:
            added_cart.total_amount = int(added_cart.product_quantity) * variant_for_cart.price
        added_cart.save()

    user_cart_all = Cart_Items.objects.filter(cart = user_cart)

    return redirect('shop:cart')


@login_required
def minus_quantity(request, product_id, attribute):

    for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=True):
        each_cart.checkout_status = False
        each_cart.save()


    product = Product.objects.filter(product_id=product_id).first()
    attribute = Attribute.objects.filter(attribute=attribute).first()
    variant_for_cart = ProductVariant.objects.get( variant=product, attribute = attribute)

    user_cart = Cart.objects.get(author=request.user, cart_ordered = False)
    cart_query = Cart_Items.objects.filter(cart = user_cart, product_variant = variant_for_cart)

    if cart_query.first():

        cart_query = Cart_Items.objects.get(cart = user_cart, product_variant = variant_for_cart)
        if int(cart_query.product_quantity) >= 1:
            cart_query.product_quantity = int(cart_query.product_quantity) - 1  # change field
            variant_for_cart.num_available = int(variant_for_cart.num_available) + 1
            cart_query.item_hold_time = datetime.now()
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

    return redirect('shop:cart')


@login_required
def cart(request):

    cart_hold_disclaimer = HtmlField.objects.filter(hf_name='cart_hold_disclaimer').first()

    user_cart = Cart.objects.filter(author=request.user, cart_ordered = False).first()

    print("Cart", user_cart)

    user_cart_all = Cart_Items.objects.filter(cart = user_cart)

    print("UserCart_all",user_cart_all)

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

        cart_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('total_amount'))['total_amount__sum']
        cart_savings_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('savings'))['savings__sum']
        cart_grand_total = Cart_Items.objects.filter(cart = user_cart).aggregate(Sum('grand_total_item'))['grand_total_item__sum']

        print("Cart Total", cart_total)
        user_cart.cart_total = cart_total
        user_cart.cart_savings_total = cart_savings_total
        user_cart.grand_total = cart_grand_total
        user_cart.save()

    context = {'cart_hold_disclaimer':cart_hold_disclaimer.hf_value,
                'user_cart':user_cart_all, 'cart':user_cart,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),}

    return render(request, 'app/cart.html', context)


@login_required
def checkout_address(request):

    address_query = DeliveryAddress.objects.filter(author=request.user)
    subs_query = SubscriptionList.objects.filter(subscribe_user=request.user)

    if request.method == "POST":
        for each_cart in Cart.objects.filter(cart_ordered=False, author=request.user, checkout_status=False):
            each_cart.checkout_status = True
            each_cart.save()
        print("this")
        if request.POST.get("fullname"):
            fullname = request.POST.get("fullname")
            print(fullname)
        if request.POST.get("mobilenumber"):
            mobilenumber = request.POST.get("mobilenumber")
            print(mobilenumber)
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
            address_query.save()
            print("Already exists")
            # context ={'address_query':address_query}
            # return render(request, 'app/checkout.html', context)

        else:
            print("Does not exist")
            DeliveryAddress.objects.create(author=request.user, full_name = fullname, mobile_number = mobilenumber, province = province, city = city, address = address)

        return redirect('shop:cart')


    address_query = DeliveryAddress.objects.filter(author=request.user)

    if address_query.first():
        print("Already exists")
        print(address_query)
        context = {'address_query':address_query.first(),
                  'subs_query':subs_query.first(),
                  'sub_sub_categories': Sub_Sub_Category.objects.all(),
                   'sub_categories':Sub_Category.objects.all(),
                    'categories': Category.objects.all(),
                    'all_brands':Brand.objects.all(),}

        # return redirect('shop:cart')
        context ={'address_query':address_query.first(),
                  'subs_query':subs_query.first(),
              'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all()}
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
            send_mail(subject, message, 'iyraseshop@gmail.com', ['saba.siddiqui.2010@gmail.com'], fail_silently=False)
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

    cart_hold_disclaimer = HtmlField.objects.filter(hf_name='cart_hold_disclaimer').first()

    address_query = DeliveryAddress.objects.filter(author=request.user)
    user_cart = Cart.objects.filter(author=request.user,cart_ordered = False).first()

    if address_query.first():

        user_cart_all = Cart_Items.objects.filter(cart = user_cart)

        context = {'address_query': address_query.first(), 'user_cart':user_cart_all, 'cart':user_cart,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories':Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),
               'cart_hold_disclaimer':cart_hold_disclaimer.hf_value,}

        return render(request, 'app/order_summary.html', context)

    else:
        return render(request, 'app/checkout.html')

    return render(request, 'app/checkout.html')

@login_required
def placeorder(request):
    # update cart Item times

    user_cart = Cart.objects.filter(author=request.user,cart_ordered = False)
    user_address = DeliveryAddress.objects.get(author=request.user)

    if user_cart.first():
        user_cart = Cart.objects.filter(author=request.user,cart_ordered = False).first()
        UserOrder.objects.create(author = request.user, order_cart = user_cart, order_address = user_address)
        user_cart.cart_ordered = True
        user_cart_all = Cart_Items.objects.filter(cart=user_cart)
        user_cart.save()

        context = {'user_cart': user_cart_all,
                   'cart': user_cart,
                   'sub_sub_categories': Sub_Sub_Category.objects.all(),
                   'sub_categories':Sub_Category.objects.all(),
                   'categories': Category.objects.all(),
                   'all_brands':Brand.objects.all(),}
        return render(request, 'app/placeorder.html', context)

    else:
        return HttpResponse('Nothing to order')


@login_required
def myorders(request):

    user_orders = UserOrder.objects.filter(author=request.user)
    user_cart = Cart.objects.filter(author=request.user)

    cart_items =[]
    for each_value in user_cart:
        cart_items.append(each_value.id)

    user_cart_all = Cart_Items.objects.filter(cart__id__in=cart_items)

    context = {'user_orders': user_orders,
               'user_cart': user_cart,
               'user_cart_all': user_cart_all,
               'sub_sub_categories': Sub_Sub_Category.objects.all(),
               'sub_categories': Sub_Category.objects.all(),
               'categories': Category.objects.all(),
               'all_brands':Brand.objects.all(),}

    return render(request, 'app/myorders.html', context)

