import django
# from django.conf import settings
# from shop import shop_defaults

import sys, os
path = '/home/iyraseshop/iyraseshop'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chart_shirt.settings")
django.setup()


from shop.models import ProductVariant, Category

all_variants = ProductVariant.objects.all()
for each_variant in all_variants:
    # print("Category", each_variant.variant.category)
    # print("Attribute Category" , each_variant.attribute,each_variant.attribute.attribute_category)
    if each_variant.variant.category == each_variant.attribute.attribute_category:
        pass
    else:
        print("Different",each_variant,each_variant.variant.category,each_variant.attribute.attribute_category)
        # each_variant.attribute.attribute_category = each_variant.variant.category
        # each_variant.attribute.save()
        # each_variant.save()
        # print("Switched to",each_variant,each_variant.variant.category,each_variant.attribute.attribute_category)

