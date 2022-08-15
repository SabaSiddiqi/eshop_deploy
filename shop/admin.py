from django.contrib import admin
from shop.models import *
from django.contrib.admin import ModelAdmin

# Register your models here.
class UserOrderAdmin(admin.ModelAdmin):
    list_filter = ('tcsorder',)


admin.site.register(Product)
admin.site.register(UserOrder, UserOrderAdmin)
admin.site.register(OrderUpdate)
admin.site.register(ContactUs)
admin.site.register(Image)
admin.site.register(ImageAlbum)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Sub_Sub_Category)
admin.site.register(ProductVariant)
admin.site.register(Attribute)
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

list_display = ('tcsorder',)
search_fields = ('tcsorder',)
list_filter = ('tcsorder',)


#
# class UserOrderAdmin(admin.ModelAdmin):
#     list_display = ('tcsorder',)
#     list_filter = ('tcsorder',)

