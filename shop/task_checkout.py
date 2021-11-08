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
