from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields ={'slug':('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields ={'slug':('name',)}





