from django.contrib import admin
from shop.models import *
from django.contrib.admin import ModelAdmin

# Register your models here.
class UserOrderAdmin(admin.ModelAdmin):
    list_filter = ('tcsorder',)

class ImageAlbumAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product_id',)


admin.site.register(Product, ProductAdmin)
admin.site.register(UserOrder, UserOrderAdmin)
admin.site.register(OrderUpdate)
admin.site.register(ContactUs)
admin.site.register(Image)
admin.site.register(ImageAlbum, ImageAlbumAdmin)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Sub_Sub_Category)
admin.site.register(ProductVariant,)
# admin.site.register(Attribute)



admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(Cart_Items)
admin.site.register(DeliveryAddress)
admin.site.register(SocialDeliveryAddress)
admin.site.register(Constants)
admin.site.register(HtmlField)
admin.site.register(Banner)
admin.site.register(SubscriptionList)
admin.site.register(Logo)
admin.site.register(DeliveryTime)
admin.site.register(Promo_Code)
admin.site.register(Returns)
admin.site.register(TCSPaymentPeriod)
admin.site.register(Shipment)
admin.site.register(SizeBucket)
admin.site.register(SizeName)
# admin.site.register(MainOrder)
# admin.site.register(Size)
list_display = ('tcsorder',)
search_fields = ('tcsorder',)
list_filter = ('tcsorder',)

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'attribute_category')
admin.site.register(Attribute, AttributeAdmin)


#
# class UserOrderAdmin(admin.ModelAdmin):
#     list_display = ('tcsorder',)
#     list_filter = ('tcsorder',)
