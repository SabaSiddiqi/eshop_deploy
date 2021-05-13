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