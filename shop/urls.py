from django.contrib import admin
from django.urls import path, include, re_path
from shop import views
from shop.views import start

app_name = 'shop'

urlpatterns = [
    path('', views.shopHome, name='ShopHome'),
<<<<<<< HEAD
=======
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
>>>>>>> bfa9342ef85418fe623d8643d9f0e568b2766dc2
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/<str:attribute>/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:product_id>/<str:attribute>/', views.remove_item, name='remove_item'),
    path('add_quantity/<int:product_id>/<str:attribute>/', views.add_quantity, name='add_quantity'),
    path('minus_quantity/<int:product_id>/<str:attribute>/', views.minus_quantity, name='minus_quantity'),
    path('check_cart/', views.check_carts, name='check_carts'),
    path('searchbycategory/<str:category>/', views.filter_by_cat, name='filter_by_cat'),
    path('searchbybrand/<str:brand>/', views.filter_by_brand, name='filter_by_brand'),
    path('searchby/<str:category>/<str:sub_category>/', views.filter_by_subcat, name='filter_by_subcat'),
    path('checkout/address/', views.checkout_address, name='checkout_address'),
    path('checkout/summary/', views.order_summary, name='order_summary'),
    path('checkout/placeorder/', views.placeorder, name='placeorder'),
    path('myorders/', views.myorders, name='myorders'),
    path('contactus/', views.contact_us, name='contact_us'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
<<<<<<< HEAD
=======

>>>>>>> bfa9342ef85418fe623d8643d9f0e568b2766dc2
    path('shipping/', views.shipping, name='shipping'),
    path('paymentmethods/', views.payment_methods, name='payment_methods'),
    path('termsconditions/', views.terms_conditions, name='termsconditions'),
    path('aboutus/', views.aboutus, name='aboutus'),
<<<<<<< HEAD
    path('productview/<int:id>/', views.productview, name='productview'),
=======


    path('tracker/', views.tracker, name='tracker'),
    path('search/', views.search, name='search'),
    path('productview/<int:id>/', views.productview, name='productview'),
    path('product-view/', views.product_view, name='product_view'),
    # re_path(r'^product-view/(?P<username>\w{0,50})/$', views.product_view, name='product_view'),
    path('allproduct/', views.allproduct, name='allproduct'),
    path('cheackout/', views.cheackout, name='cheackout'),
    # path('sentemail/', views.sentemail, name='sentemail'),
    path('man/', views.man, name='man'),
    path('woman/', views.woman, name='woman'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('gen_pdf/', views.gen_pdf, name='gen_pdf'),
>>>>>>> bfa9342ef85418fe623d8643d9f0e568b2766dc2
]


start()
