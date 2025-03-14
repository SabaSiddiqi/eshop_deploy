from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
# from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models
from django.conf import settings
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager

def get_upload_path(instance, filename):
    title = instance.album.name
    # slug = slugify(title)
    return "images/%s/%s" % (title,filename)

def get_icon_upload_path(instance, filename):
    title = instance.album.name
    # slug = slugify(title)
    print("Upload to", filename)
    return "images/%s/icon/%s" % (title,filename)

def get_real_upload_path(instance, filename):
    title = instance.album.name
    # slug = slugify(title)
    print("Upload to", filename)
    return "images/%s/real/%s" % (title,filename)

class Banner(models.Model):
    banner_text = models.CharField(max_length=255)
    banner_image = models.ImageField(upload_to='banner', null=True)

class Logo(models.Model):
    logo_text = models.CharField(max_length=255)
    logo_image = models.ImageField(upload_to='logo', null=True)

class SubscriptionList(models.Model):
    subscribe_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    subscribe_date_time = models.DateTimeField(auto_now=True,null=True,blank=True)
    subscribe_status = models.BooleanField(default=False)

class HtmlField(models.Model):
    hf_name = models.CharField(max_length=255)
    hf_value = models.TextField( null=True, blank=True)
    my_field = tinymce_models.HTMLField(blank=True)

class ImageAlbum(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    name = models.CharField(max_length=255, default="name")
    image = models.ImageField(upload_to=get_upload_path, null=True)
    default = models.BooleanField(default=False)
    # width = models.FloatField(default=100)
    # length = models.FloatField(default=100)
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE,null=True)
    icon_image = models.ImageField(upload_to=get_icon_upload_path, null=True, blank=True)
    real_image = models.ImageField(upload_to=get_real_upload_path, null=True, blank=True)

    def __str__(self):
        print("Image",self.image)
        return self.name

class Category(models.Model):
    # cat_id = models.AutoField(primary_key=True,)
    cat_name = models.CharField(max_length=225,unique=True)
    cat_slug = AutoSlugField(populate_from='cat_name', blank=True)
    cat_des = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.cat_name

class Sub_Category(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    sub_cat_name = models.CharField(max_length=225, null=True)
    sub_slug = AutoSlugField(populate_from='sub_cat_name', blank=True)
    sub_cat_des = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.sub_cat_name

class Sub_Sub_Category(models.Model):

    sub_cat = models.ForeignKey(Sub_Category, on_delete=models.CASCADE,null=True)
    sub_sub_cat_name = models.CharField(max_length=225, null=True)
    sub_sub_slug = AutoSlugField(populate_from='sub_sub_cat_name',blank=True)
    sub_sub_cat_des = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.sub_sub_cat_name


class Constants(models.Model):
    constant_name = models.CharField(max_length=225)
    constant_value = models.CharField(max_length=225)
    def __str__(self):
        return self.constant_name


class Brand (models.Model):
    # cat_id = models.AutoField(primary_key=True,)
    brand_name = models.CharField(max_length=225, null=True, default="Brand")
    brand_des = models.CharField(max_length=250, null=True)
    brand_slug = AutoSlugField(populate_from='brand_name', blank=True, null=True)
    brand_name = models.CharField(max_length=225, null = True, default = "Brand")
    brand_des = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.brand_name


class MainOrder (models.Model):
    order_date = models.DateField(null=True, blank=True)
    order_number = models.CharField(max_length=255, null=True, blank=True)
    order_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return '{} - {} - {}'.format(self.order_date, self.order_number, self.order_brand)



class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_sub_category = models.ForeignKey(Sub_Sub_Category, on_delete=models.CASCADE, null=True, blank=True)
    product_tags = TaggableManager(blank=True)


    price = models.IntegerField(null=True, blank=True)
    apply_discount = models.BooleanField(default=False, blank=True)
    discount_percent = models.IntegerField(null=True, blank=True)
    discounted_price = models.IntegerField(blank=True, null=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)

    publish_date = models.DateField(null=True, blank=True)

    image = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, blank=True)
    is_published = models.BooleanField(default=True, blank=True)
    on_sale = models.BooleanField(default=False, blank=True)
    is_preorder = models.BooleanField(default=False, blank=True)



    #added this
    AVAILABILITY_CHOICES = (
        ('InStock', 'InStock'),
        ('SoldOut', 'SoldOut'),
        ('PreOrder', 'PreOrder'),)
    availability_type = models.CharField(max_length=255, choices=AVAILABILITY_CHOICES, default='InStock')



    product_views=models.IntegerField(default=0, null=True, blank=True)
    hit_count_generic = GenericRelation( HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation' )




    def __str__(self):
        return '{} - {}'.format(self.product_id, self.product_name)
        # return f"{self.product_id} - {self.product_name}"

class DeliveryTime (models.Model):
    delivery_time = models.CharField(max_length=250, null=True, blank=True,unique=True)

    def __str__(self):

        return self.delivery_time

class SizeName(models.Model):
    size_name = models.CharField(max_length=255, default='Newborn')
    size_slug = AutoSlugField(populate_from='size_name', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.size_name)

class Attribute (models.Model):
    attribute = models.CharField(max_length=250, null=True, blank=True)
    attribute_slug = AutoSlugField(populate_from='attribute', blank=True, null=True)
    attribute_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # return '{} - {}'.format(self.attribute, self.attribute_category)
        return self.attribute

class SizeBucket(models.Model):
    size_name = models.ForeignKey(SizeName, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.size_name, self.attribute)


class Shipment(models.Model):
    shipment = models.IntegerField(default=1)
    shipment_charges = models.FloatField(blank=True, null=True)
    number_of_items = models.FloatField(blank=True, null=True)
    shipment_charges_per_item = models.FloatField(blank=True, null=True)
    shipment_rate = models.FloatField(default=158, blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.number_of_items:
            self.shipment_charges_per_item = self.shipment_charges / self.number_of_items

        return super(Shipment, self).save()

    def __str__(self):

        return '{}'.format(self.shipment)

class ProductVariant(models.Model):

    main_order = models.ForeignKey(MainOrder, on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    delivery_time = models.ForeignKey(DeliveryTime, on_delete=models.CASCADE, null=True, blank=True)

    buy_price = models.FloatField(blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)

    apply_discount = models.BooleanField(default=False, blank=True)
    discount_percent = models.IntegerField(null=True, blank=True)
    discounted_price = models.IntegerField(blank=True, null=True)

    total_pcs = models.IntegerField(default=1, null=True, blank=True)
    num_available = models.IntegerField(default=1)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True, blank=True)
    shipment_charges = models.FloatField(default=1,blank=True, null=True)

    savings_item = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.shipment.number_of_items:
            self.shipment_charges = self.shipment.shipment_charges_per_item
        else:
            self.shipment_charges = 1

        if self.apply_discount:
            # self.discounted_price = self.price - (self.price * self.discount_percent / 100)
            self.savings_item = self.price - self.discounted_price

        else:
            self.savings_item = 0
            # self.discounted_price = self.price

        return super(ProductVariant, self).save()

    def __str__(self):
        return '{} - {}'.format(self.variant, self.attribute)

        # return f"{self.variant} - {self.attribute}"

#cart notifications
#save for only two hours
class Cart (models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    cart_total = models. IntegerField(default=0, blank=True, null=True)
    promo_cart_total = models. IntegerField(default=0, blank=True, null=True)
    cart_ordered = models.BooleanField(default=False)
    delivery_charges = models.IntegerField(default=0, blank=True, null=True)
    grand_total = models. IntegerField(default=0, blank=True, null=True)
    cart_savings_total = models. IntegerField(default=0, blank=True, null=True)
    cart_promo_savings = models. IntegerField(default=0, blank=True, null=True)
    #update this one
    checkout_status = models.BooleanField(default=False)
    checkout_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    #update this one
    cart_promo_flag = models.BooleanField(default=False, null=True, blank=True)
    delivery_charges = models.FloatField(null=True, blank=True)
    tcs_delivery_charges = models.FloatField(null=True, blank=True)
    delivery_charges_per_item = models.FloatField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #
    #     #
    #     #
    #     # if self.promo_cart_total > 2999:
    #     #     self.delivery_charges = 0
    #     #     self.promo_cart_total = self.promo_cart_total + self.delivery_charges
    #     # else:
    #     #     self.delivery_charges = 250
    #     #     self.promo_cart_total = self.promo_cart_total + self.delivery_charges
    #
    #     if self.cart_total > 2999:
    #         self.delivery_charges = 0
    #         self.cart_total = self.cart_total + self.delivery_charges
    #     else:
    #         self.delivery_charges = 250
    #         self.cart_total = self.cart_total + self.delivery_charges
    #
    #     return super(Cart, self).save()

    def __str__(self):
        return '{} - {}'.format(self.author, self.cart_ordered)


class Promo_Code (models.Model):
    PROMO_CHOICES = (
        ('one_time', 'ONE_TIME'),
        ('on_demand', 'ON_DEMAND'),
        ('tag_based', 'TAG_BASED'))
    promo_type = models.CharField(max_length=255, choices=PROMO_CHOICES, default='one_time')
    promo_name = models.CharField(max_length=255)
    promo_code = models.CharField(max_length=255)
    promo_percent = models.IntegerField()
    promo_status = models.BooleanField(default=False)
    promo_text = models.CharField(max_length=255, null=True, blank=True)
    promo_tag = models.CharField(max_length=255, null=True, blank=True)

    def save(self):
        if self.promo_type == 'tag_based' and self.promo_status == True:
            print("Add Tag")
            for each_product in Product.objects.all():
                for each_tag in each_product.product_tags.all():
                    if self.promo_tag == each_tag.name:
                        each_product.on_sale = True
                        each_product.save()
                    print(each_tag, "Add Sale -->", each_product.on_sale)
            return super(Promo_Code, self).save()

        if self.promo_type == 'tag_based' and self.promo_status == False:
            print("Remove Tag")
            for each_product in Product.objects.all():
                for each_tag in each_product.product_tags.all():
                    if self.promo_tag == each_tag.name:
                        each_product.on_sale = False
                        each_product.save()
                    # print(each_tag, "Remove Sale-->", each_product.on_sale)
            return super(Promo_Code, self).save()

        if self.promo_type == 'on_demand' and self.promo_status == True:
            print("Add on demand")
            for each_product in Product.objects.all():
                each_product.on_sale = True
                each_product.save()

            return super(Promo_Code, self).save()

        if self.promo_type == 'on_demand' and self.promo_status == False:
            print("Remove on demand")
            for each_product in Product.objects.all():
                each_product.on_sale = False
                each_product.save()
            return super(Promo_Code, self).save()


class Cart_Items (models.Model):
    cart = models.ForeignKey(Cart ,on_delete=models.CASCADE, blank=True, null=True)
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE, blank=True, null=True)
    product_quantity = models.IntegerField(default=0, blank=True, null=True)
    add_date_time = models.DateTimeField(auto_now=True,null=True,blank=True)
    item_price = models.IntegerField(default=0, blank=True, null=True)
    item_discount_percent = models.IntegerField(default=0, blank=True, null=True)
    item_discount_price = models.IntegerField(default=0, blank=True, null=True)
    total_amount = models.IntegerField(default=0, blank=True, null=True)
    promo_unit_amount = models.IntegerField(default=0, blank=True, null=True)
    promo_total_amount = models.IntegerField(default=0, blank=True, null=True)
    savings = models.IntegerField(default=0, blank=True, null=True)
    grand_total_item = models.IntegerField(default=0, blank=True, null=True)
    item_hold_time = models.DateTimeField(null=True, blank=True)
    promo_savings = models.IntegerField(default=0, blank=True, null=True)
    total_saving = models.IntegerField(default=0, blank=True, null=True)
    returned = models.BooleanField(default=False)

    delivery_charges_per_item = models.FloatField(blank=True, null=True)
    profit_cad = models.FloatField(blank=True, null=True)
    profit_pkr = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.cart.cart_promo_flag:
            if self.cart.tcs_delivery_charges:
                self.delivery_charges_per_item = self.cart.delivery_charges_per_item
                self.profit_cad = ((self.total_amount-self.delivery_charges_per_item)/self.product_variant.shipment.shipment_rate) - self.product_variant.buy_price
                self.profit_pkr = (self.total_amount-self.delivery_charges_per_item) - (self.product_variant.buy_price*self.product_variant.shipment.shipment_rate)
        else:
            if self.cart.tcs_delivery_charges:
                self.delivery_charges_per_item = self.cart.delivery_charges_per_item
                self.profit_cad = ((self.promo_total_amount-self.delivery_charges_per_item)/self.product_variant.shipment.shipment_rate) - self.product_variant.buy_price
                self.profit_pkr = (self.promo_total_amount-self.delivery_charges_per_item) - (self.product_variant.buy_price*self.product_variant.shipment.shipment_rate)

        if self.cart.tcs_delivery_charges:
            self.delivery_charges_per_item = self.cart.delivery_charges_per_item
            self.profit_cad = ((self.total_amount-self.delivery_charges_per_item)/self.product_variant.shipment.shipment_rate) - self.product_variant.buy_price
            self.profit_pkr = (self.total_amount-self.delivery_charges_per_item) - (self.product_variant.buy_price*self.product_variant.shipment.shipment_rate)

        if self.add_date_time:
            # print("Add Date", self.add_date_time)
            d = self.add_date_time
            # print(d)
            # print(d.strftime("%Y-%m-%d %H:%M:%S"))
            # print(timezone.localtime(d).strftime("%Y-%m-%d %H:%M:%S"))
            self.add_date_time = timezone.localtime(d).strftime("%Y-%m-%d %H:%M:%S")
        else:
            print("None returned")
        # self.add_date_time = dateformat.format(self.add_date_time, 'Y-m-d H:i:s')
        return super(Cart_Items, self).save()

    def __str__(self):
        return '{} - {}'.format(self.cart, self.product_variant)


class DeliveryAddress(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=50,null=True, blank=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.author, self.full_name)


class SocialDeliveryAddress(models.Model):
    username = models.CharField(max_length=255)
    MEDIA_CHOICES = (
    ('instagram', 'INSTAGRAM'),
    ('facebook', 'FACEBOOK'),)
    media_type = models.CharField(max_length=255, choices=MEDIA_CHOICES, default='instagram')
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=50,null=True, blank=True)
    province = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {} - {}'.format(self.username, self.full_name, self.mobile_number)


class TCSPaymentPeriod(models.Model):
    payment_period = models.CharField(max_length=255, blank=True)
    booking_date = models.DateField(null=True, blank=True)
    delivery_charges = models.FloatField(null=True, blank=True)
    cod_total = models.IntegerField(blank=True, null=True)
    cod_return = models.IntegerField(blank=True, null=True)
    number_of_orders = models.IntegerField(blank=True, null=True)
    delivery_per_order = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.number_of_orders:
            self.delivery_per_order = (self.cod_total-self.cod_return)/self.number_of_orders
        return super(TCSPaymentPeriod, self).save()

    def __str__(self):
        return '{}'.format(self.payment_period)

class UserOrder(models.Model):

    STATUS_CHOICES = (
        ('active', 'ACTIVE'),
        ('shipped', 'SHIPPED'),
        ('deliver', 'DELIVERED'),
        ('returned', 'RETURNED'),
        ('cancelled', 'CANCELLED'),
    )

    PAYMENT_TYPE = (
        ('cod', 'COD'),
        ('bank_transfer', 'BANK TRANSFER'),
        ('gift', 'GIFT'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    tcsorder = models.ForeignKey(TCSPaymentPeriod,on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.AutoField(primary_key=True)
    order_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    order_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE, blank=True, null=True)
    social_address = models.ForeignKey(SocialDeliveryAddress, on_delete=models.CASCADE, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='active')
    payment_type = models.CharField(max_length=255, choices=PAYMENT_TYPE, default='cod')
    tracking_id = models.CharField(max_length=255, blank=True)
    booking_date = models.DateField(null=True, blank=True)
    delivery_charges = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.tcsorder:
            self.delivery_charges = self.tcsorder.delivery_per_order
            self.order_cart.tcs_delivery_charges = self.delivery_charges
            cart_item_count = len(Cart_Items.objects.filter(cart=self.order_cart))
            self.order_cart.delivery_charges_per_item = self.delivery_charges/cart_item_count
            print(self.order_cart.delivery_charges_per_item)
            self.order_cart.save()
        return super(UserOrder, self).save()




    def __str__(self):
        return '{} - {} ---- [{}]'.format(self.author, self.order_id, self.social_address)


class Returns (models.Model):
    return_item = models.ForeignKey(Cart_Items ,on_delete=models.CASCADE, blank=True, null=True)
    return_cost = models.IntegerField(default=0, blank=True, null=True)
    return_reason = models.CharField(max_length=50,null=True, blank=True)
    return_date = models.DateTimeField(auto_now=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.return_date:
            d = self.return_date
            self.return_date = timezone.localtime(d).strftime("%Y-%m-%d %H:%M:%S")
        return super(Returns, self).save()


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    status = models.CharField(max_length=255, default="")
    update_desc = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.order_id, self.status)

        # return f"{self.order_id} - {self.status}"


class ContactUs(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):

        return '{} - {}'.format(self.contact_id, self.name)
        # return f"{self.contact_id} - {self.name}"
