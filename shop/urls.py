from django.contrib import admin
from django.urls import path, include, re_path
from shop import views
# from shop.views import start

app_name = 'shop'

urlpatterns = [
    path('', views.shopHome, name='ShopHome'),
    path('cart/', views.cart, name='cart'),
    path('preorder/', views.preorder, name='preorder'),
    path('add_to_cart/<int:product_id>/<str:attribute_slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:product_id>/<str:attribute>/', views.remove_item, name='remove_item'),
    path('add_quantity/<int:product_id>/<str:attribute>/', views.add_quantity, name='add_quantity'),
    path('minus_quantity/<int:product_id>/<str:attribute>/', views.minus_quantity, name='minus_quantity'),
    path('check_cart/', views.check_carts, name='check_carts'),

    path('searchbycategory/<str:category>/', views.filter_by_cat, name='filter_by_cat'),
    path('searchbycategory/<str:category>/<str:size>/', views.filter_by_cat_and_size, name='filter_by_cat_and_size'),
    path('searchbytag/<str:tag>/', views.filter_by_tag, name='filter_by_tag'),
    path('searchbybrand/<str:brand>/', views.filter_by_brand, name='filter_by_brand'),
    path('searchbybrand/<str:brand>/<str:size>/', views.filter_by_brand_and_size, name='filter_by_brand_and_size'),

    path('searchbycategorypreorder/<str:category>/', views.filter_by_cat_preorder, name='filter_by_cat_preorder'),
    path('searchbycategorypreorder/<str:category>/<str:size>/', views.filter_by_cat_and_size_preorder, name='filter_by_cat_and_size_preorder'),
    path('searchbytagpreorder/<str:tag>/', views.filter_by_tag_preorder, name='filter_by_tag_preorder'),
    path('searchbybrandpreorder/<str:brand>/', views.filter_by_brand_preorder, name='filter_by_brand_preorder'),
    path('searchbybrandpreorder/<str:brand>/<str:size>/', views.filter_by_brand_and_size_preorder, name='filter_by_brand_and_size_preorder'),
    path('shopallpreorders/', views.shop_all_preorder, name='shop_all_preorder'),


    path('searchby/<str:category>/<str:sub_category>/', views.filter_by_subcat, name='filter_by_subcat'),
    path('checkout/address/', views.checkout_address, name='checkout_address'),
    path('checkout/summary/', views.order_summary, name='order_summary'),
    path('checkout/placeorder/', views.placeorder, name='placeorder'),
    path('myorders/', views.myorders, name='myorders'),
    path('allorders/', views.allorders, name='allorders'),
    path('summary/', views.summary, name='summary'),
    path('contactus/', views.contact_us, name='contact_us'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('shipping/', views.shipping, name='shipping'),
    path('paymentmethods/', views.payment_methods, name='payment_methods'),
    path('termsconditions/', views.terms_conditions, name='termsconditions'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('imageupload/', views.product_image_upload, name='imageupload'),

    path('productadd/', views.product_add, name='productadd'),
    path('inventoryadd/', views.inventory_add, name='inventoryadd'),
    # path('mainorders/', views.main_orders_summary, name='main_orders_summary'),
    path('productupdate/<int:product_id>/', views.product_update, name='productupdate'),


    path('removevariant/<int:variant_id>/', views.remove_variant, name='removevariant'),
    path('addvariant/<int:product_id>/', views.add_variant, name='addvariant'),

    path('solditems/', views.solditems, name='solditems'),
    path('returnitem/<int:variant_id>/', views.returnitem, name='returnitem'),

    path('productview/<int:id>/', views.productview, name='productview'),
    path('productview/<int:id>/<str:attribute_slug>/', views.productview_details, name='productview_details'),

    path('admindash/', views.admin_dashboard, name='admindash'),
    path('admindash/<int:id>/', views.shipment_dashboard, name='shipment_dashboard'),
    path('publish/<int:product_id>/', views.publish, name='publish'),
    path('unpublish/<int:product_id>/', views.unpublish, name='unpublish'),
    path('showimages/', views.show_images, name='show_images'),


]


