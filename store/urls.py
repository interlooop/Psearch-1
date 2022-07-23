from django.urls import path, register_converter
from . import views,converters

register_converter(converters.EmptyOrSlugConverter, 'emptyorslug')

urlpatterns = [
    path('', views.store, name="store"),
    
    path('checkout/', views.checkout, name="checkout"),
    path('checkout-payment/', views.checkout, name="checkout-payment"),
    
    path('checkout/payment-complete/', views.paymentComplete, name="payment-complete"),
    path('payment-successful', views.paymentSuccessful, name="payment-successful"),
    
    path('<slug:product_slug>/', views.singleProduct, name="single-product"),
    path('category/<emptyorslug:category_slug>/', views.products, name="products-by-category"),

]
