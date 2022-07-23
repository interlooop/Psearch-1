from .cart import Cart
from store.models import *
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def cart(request):
    return {'cart': Cart(request)}

