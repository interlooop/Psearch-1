from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
# Create your models here.

class Customer(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True,blank=True)
    name=models.CharField(max_length=200,null=True,validators=[alphanumeric])
    email=models.EmailField(max_length=500, null=True)


    def __str__(self):
        return str(self.name)



class Category(models.Model):
    CATEGORY_VALUE=(
        ('Clothes','clothes'),
        ('Software','software') ,
        ('Books','books'),
        ('Other','other')
        
    )
    name = models.CharField(max_length=200,choices=CATEGORY_VALUE)
    slug = models.SlugField(max_length=200, unique=True)
    
    

    class Meta:
        ordering=('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products-by-category', args=[self.slug])



class Product(models.Model):
    
    name=models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200, unique=True)
    price=models.DecimalField(max_digits=7,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    qtyInStock=models.PositiveIntegerField(null=True,blank=True,default=10)
    reservedQuantity=models.PositiveIntegerField(null=True,blank=True,default=0)
    digital=models.BooleanField(default=False, null=True, blank=False)
    category=models.ForeignKey('Category',related_name='categories' ,null=True,blank=False, on_delete=models.CASCADE)
    image=models.ImageField(null=True,blank=True, upload_to="store-images/",default="store-images/default.jpg")


    def __str__(self):
        return self.name

    class Meta:
        ordering=['name']
    

    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url='/images/store-images/default.jpg'
        return url


    @property
    def availableQuantity(self):
        if self.qtyInStock >= self.reservedQuantity:
            availableQuantityForPurchase=self.qtyInStock-self.reservedQuantity
        else:
            availableQuantityForPurchase=0
            
        return availableQuantityForPurchase


class ShippingAddress(models.Model):
    
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True,validators=[alphanumeric])
    state=models.CharField(max_length=200,null=True,validators=[alphanumeric])
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address


class Order(models.Model):
    
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    shipping_address=models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, null=True, blank=False)
    transaction_id=models.CharField(max_length=200,null=True)


    def __str__(self):
        return str(self.id)


    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping=True
        return shipping

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0, null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.product:
            return str(self.product.name)
        else:
            pass

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total

