import django
# from django.conf import settings
# from shop import shop_defaults

import sys, os
path = '/home/iyraseshop/iyraseshop'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chart_shirt.settings")
django.setup()


from shop.models import Cart, ProductVariant, Cart_Items, Constants
from datetime import datetime

print("I'm in checkout task now")



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


#for cart items that are in checkout state but card is not ordered
for each_cart in Cart.objects.filter(cart_ordered=False, checkout_status=True):
    for each_item in Cart_Items.objects.filter(cart=each_cart):
        #get variant
        variant_for_cart = ProductVariant.objects.get(variant=each_item.product_variant.variant.product_id, attribute = each_item.product_variant.attribute)
        #get quantity
        quantity = int(each_item.product_quantity)
        #Delete from Cart
        Cart_Items.objects.filter(cart = each_cart, product_variant = each_item.product_variant).delete()
        #update number of items
        variant_for_cart.num_available = int(variant_for_cart.num_available) + quantity
        #save cart
        variant_for_cart.save()
        update_soldout_product(each_item.product_variant.variant)



